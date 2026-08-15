import os
import sqlite3
from contextlib import closing
from datetime import datetime
from typing import Optional, List, Dict, Any


class Database:
    def __init__(self, db_path: str = "monitor_guias.db"):
        self.db_path = db_path
        self.init_db()

    def get_connection(self) -> sqlite3.Connection:
        """Retorna conexÃ£o com banco SQLite com configuraÃ§Ãµes anti-lock."""
        conn = sqlite3.connect(
            self.db_path,
            timeout=30,              # espera atÃ© 30s se estiver ocupado
            check_same_thread=False  # evita erro em contextos com mÃºltiplas threads
        )
        conn.row_factory = sqlite3.Row

        # pragmas para reduzir lock
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        conn.execute("PRAGMA foreign_keys=ON;")
        conn.execute("PRAGMA busy_timeout=30000;")  # 30s
        return conn

    def init_db(self):
        """Inicializa o banco de dados com schema"""
        with closing(self.get_connection()) as conn:
            cursor = conn.cursor()

            # Tabela de Guias
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS guides (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    numero_guia TEXT NOT NULL UNIQUE,
                    paciente TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'Guia emitida / liberada',
                    ultima_consulta TIMESTAMP,
                    ultima_alteracao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    ciencia_status TEXT DEFAULT 'Pendente',
                    ciencia_timestamp TIMESTAMP,
                    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(numero_guia)
                )
            ''')

            # Tabela de HistÃ³rico
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    guide_id INTEGER NOT NULL,
                    status_anterior TEXT,
                    status_novo TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    usuario TEXT DEFAULT 'Sistema',
                    observacoes TEXT,
                    FOREIGN KEY (guide_id) REFERENCES guides(id)
                )
            ''')

            # Tabela de ConfiguraÃ§Ãµes
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS settings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chave TEXT NOT NULL UNIQUE,
                    valor TEXT,
                    tipo TEXT,
                    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Tabela de Log de Auditoria
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS audit_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    acao TEXT NOT NULL,
                    tabela TEXT,
                    registro_id INTEGER,
                    usuario TEXT DEFAULT 'Sistema',
                    ip_address TEXT,
                    dados_anteriores TEXT,
                    dados_novos TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            conn.commit()

    def add_guide(self, numero_guia: str, paciente: str,
                  status: str = "Guia emitida / liberada") -> bool:
        """Adiciona nova guia ao banco"""
        try:
            agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            with closing(self.get_connection()) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO guides (numero_guia, paciente, status, ultima_alteracao)
                    VALUES (?, ?, ?, ?)
                ''', (numero_guia, paciente, status, agora))
                conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_all_guides(self) -> List[Dict[str, Any]]:
        """Retorna todas as guias"""
        with closing(self.get_connection()) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM guides ORDER BY ultima_alteracao DESC')
            guides = [dict(row) for row in cursor.fetchall()]
        return guides

    def get_guide_by_id(self, guide_id: int) -> Optional[Dict[str, Any]]:
        """Retorna guia por ID"""
        with closing(self.get_connection()) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM guides WHERE id = ?', (guide_id,))
            guide = cursor.fetchone()
        return dict(guide) if guide else None

    def update_guide_status(self, guide_id: int, novo_status: str) -> bool:
        """Atualiza status de uma guia"""
        agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        with closing(self.get_connection()) as conn:
            cursor = conn.cursor()

            # Pega status anterior
            cursor.execute('SELECT status FROM guides WHERE id = ?', (guide_id,))
            row = cursor.fetchone()
            status_anterior = row[0] if row else None

            # Atualiza status
            cursor.execute('''
                UPDATE guides
                SET status = ?, ultima_alteracao = ?
                WHERE id = ?
            ''', (novo_status, agora, guide_id))

            # Registra no histórico
            cursor.execute('''
                INSERT INTO history (guide_id, status_anterior, status_novo, timestamp)
                VALUES (?, ?, ?, ?)
            ''', (guide_id, status_anterior, novo_status, agora))

            conn.commit()
        return True

    def mark_as_aware(self, guide_id: int) -> bool:
        """Marca guia como ciente"""
        with closing(self.get_connection()) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE guides
                SET ciencia_status = 'Ciente', ciencia_timestamp = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (guide_id,))
            conn.commit()
        return True

    def get_history(self, guide_id: int) -> List[Dict[str, Any]]:
        """Retorna histÃ³rico de uma guia"""
        with closing(self.get_connection()) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM history
                WHERE guide_id = ?
                ORDER BY timestamp DESC
            ''', (guide_id,))
            history = [dict(row) for row in cursor.fetchall()]
        return history