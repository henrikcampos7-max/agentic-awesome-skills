"""
Histórico de Guias com Auditoria
"""

from typing import List, Dict, Any
from datetime import datetime
from src.database.schema import Database
from src.utils.logger import LGPDLogger

class HistoryService:
    """Serviço para gerenciar histórico e auditoria de guias"""
    
    def __init__(self, db: Database, logger: LGPDLogger):
        self.db = db
        self.logger = logger
    
    def get_guide_history(self, guide_id: int) -> List[Dict[str, Any]]:
        """Retorna histórico completo de uma guia"""
        return self.db.get_history(guide_id)
    
    def add_history_entry(self, guide_id: int, status_anterior: str,
                         status_novo: str, usuario: str = "Sistema",
                         observacoes: str = "") -> bool:
        """Adiciona entrada no histórico"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO history (guide_id, status_anterior, status_novo, usuario, observacoes)
                VALUES (?, ?, ?, ?, ?)
            ''', (guide_id, status_anterior, status_novo, usuario, observacoes))
            conn.commit()
            conn.close()
            
            self.logger.log_guide_update(
                f"guide_id_{guide_id}",
                status_anterior,
                status_novo,
                usuario
            )
            return True
        except Exception as e:
            self.logger.log_error("HISTORY_ADD_ERROR", str(e))
            return False
    
    def get_awareness_history(self, guide_id: int) -> List[Dict[str, Any]]:
        """Retorna histórico de ciência de uma guia"""
        history = self.get_guide_history(guide_id)
        # Filtrar apenas mudanças de ciência
        # Implementar filtro específico
        return history
    
    def export_audit_log(self, filename: str = "audit_log.json") -> bool:
        """Exporta log de auditoria"""
        try:
            import json
            
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM audit_log ORDER BY timestamp DESC')
            audit_logs = [dict(row) for row in cursor.fetchall()]
            conn.close()
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(audit_logs, f, indent=2, ensure_ascii=False, default=str)
            
            self.logger.logger.info(f"AUDIT_EXPORTED | filename={filename}")
            return True
        except Exception as e:
            self.logger.log_error("AUDIT_EXPORT_ERROR", str(e))
            return False
    
    def get_user_actions(self, usuario: str, dias: int = 7) -> List[Dict[str, Any]]:
        """Retorna ações de um usuário nos últimos N dias"""
        try:
            from datetime import timedelta
            
            conn = self.db.get_connection()
            cursor = conn.cursor()
            data_limite = (datetime.now() - timedelta(days=dias)).isoformat()
            
            cursor.execute('''
                SELECT * FROM audit_log
                WHERE usuario = ? AND timestamp > ?
                ORDER BY timestamp DESC
            ''', (usuario, data_limite))
            
            actions = [dict(row) for row in cursor.fetchall()]
            conn.close()
            return actions
        except Exception as e:
            self.logger.log_error("USER_ACTIONS_ERROR", str(e))
            return []
