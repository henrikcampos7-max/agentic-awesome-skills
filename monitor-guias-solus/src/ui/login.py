"""
T27 — Tela de Login
Autenticação local com persistência de usuário via tabela settings.
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QLineEdit, QPushButton, QCheckBox, QFrame, QMessageBox
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from src.database.schema import Database

# Credenciais padrão do sistema (sem backend externo, autenticação local simples)
_USUARIOS_PADRAO = {
    "henrique.campos": "solus@2026",
    "admin": "admin123",
}

_LOGIN_STYLE = """
QDialog {
    background-color: #1a3a52;
}
QWidget#painel {
    background-color: #f5f5f5;
    border-radius: 12px;
}
QLabel {
    color: #333333;
    font-size: 13px;
}
QLabel#titulo {
    color: #1a3a52;
    font-size: 20px;
    font-weight: bold;
}
QLabel#subtitulo {
    color: #666666;
    font-size: 12px;
}
QLabel#lbl_app {
    color: #ffffff;
    font-size: 22px;
    font-weight: bold;
}
QLabel#lbl_versao {
    color: #a0c4de;
    font-size: 11px;
}
QLabel#erro {
    color: #cc0000;
    font-size: 12px;
}
QLineEdit {
    border: 1px solid #cccccc;
    border-radius: 6px;
    padding: 10px;
    background-color: white;
    color: #333333;
    font-size: 13px;
    min-height: 22px;
}
QLineEdit:focus {
    border: 2px solid #0066cc;
}
QPushButton#btn_entrar {
    background-color: #0066cc;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 12px;
    font-weight: bold;
    font-size: 14px;
}
QPushButton#btn_entrar:hover {
    background-color: #0052a3;
}
QPushButton#btn_entrar:pressed {
    background-color: #003d7a;
}
QPushButton#btn_entrar:disabled {
    background-color: #aaaaaa;
}
QCheckBox {
    color: #555555;
    font-size: 12px;
    spacing: 6px;
}
"""


class LoginDialog(QDialog):
    """
    Tela de login da aplicação Monitor de Guias Solus.

    Autentica o usuário localmente (sem servidor).
    Persiste 'lembrar usuário' na tabela settings do SQLite.

    Emite:
        login_realizado: (usuario: str) após autenticação bem-sucedida
    """

    login_realizado = Signal(str)

    def __init__(self, db: Database, parent=None):
        super().__init__(parent)
        self._db = db
        self.setWindowTitle("Monitor de Guias Solus — Login")
        self.setFixedSize(420, 520)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setModal(True)
        self.setStyleSheet(_LOGIN_STYLE)
        self._build_ui()
        self._carregar_usuario_salvo()

    def _build_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # ── Faixa superior (fundo azul escuro) ───────────────────────────────
        topo = QVBoxLayout()
        topo.setContentsMargins(30, 36, 30, 30)
        topo.setSpacing(6)

        icone = QLabel("🏥")
        icone.setFont(QFont("Arial", 36))
        icone.setAlignment(Qt.AlignCenter)
        icone.setStyleSheet("color: white;")
        topo.addWidget(icone)

        lbl_app = QLabel("Monitor de Guias Solus")
        lbl_app.setObjectName("lbl_app")
        lbl_app.setAlignment(Qt.AlignCenter)
        topo.addWidget(lbl_app)

        lbl_sub = QLabel("Farmácia Oncológica — Cacoal (RO)")
        lbl_sub.setObjectName("lbl_versao")
        lbl_sub.setAlignment(Qt.AlignCenter)
        topo.addWidget(lbl_sub)

        outer.addLayout(topo)

        # ── Painel branco com formulário ──────────────────────────────────────
        painel = QFrame()
        painel.setObjectName("painel")
        painel_layout = QVBoxLayout(painel)
        painel_layout.setContentsMargins(30, 28, 30, 28)
        painel_layout.setSpacing(14)

        lbl_titulo = QLabel("Entrar no Sistema")
        lbl_titulo.setObjectName("titulo")
        lbl_titulo.setAlignment(Qt.AlignCenter)
        painel_layout.addWidget(lbl_titulo)

        # Campos
        form = QFormLayout()
        form.setSpacing(10)
        form.setLabelAlignment(Qt.AlignLeft)

        lbl_u = QLabel("Usuário")
        lbl_u.setFont(QFont("Arial", 11))
        self.campo_usuario = QLineEdit()
        self.campo_usuario.setPlaceholderText("henrique.campos")
        self.campo_usuario.returnPressed.connect(self._tentar_login)
        form.addRow(lbl_u, self.campo_usuario)

        lbl_s = QLabel("Senha")
        lbl_s.setFont(QFont("Arial", 11))
        self.campo_senha = QLineEdit()
        self.campo_senha.setEchoMode(QLineEdit.Password)
        self.campo_senha.setPlaceholderText("••••••••")
        self.campo_senha.returnPressed.connect(self._tentar_login)
        form.addRow(lbl_s, self.campo_senha)

        painel_layout.addLayout(form)

        # Lembrar usuário
        self.chk_lembrar = QCheckBox("Lembrar meu usuário")
        painel_layout.addWidget(self.chk_lembrar)

        # Mensagem de erro (oculta por padrão)
        self.lbl_erro = QLabel("")
        self.lbl_erro.setObjectName("erro")
        self.lbl_erro.setAlignment(Qt.AlignCenter)
        self.lbl_erro.setWordWrap(True)
        self.lbl_erro.hide()
        painel_layout.addWidget(self.lbl_erro)

        painel_layout.addStretch()

        # Botão Entrar
        self.btn_entrar = QPushButton("Entrar")
        self.btn_entrar.setObjectName("btn_entrar")
        self.btn_entrar.setDefault(True)
        self.btn_entrar.clicked.connect(self._tentar_login)
        painel_layout.addWidget(self.btn_entrar)

        outer.addWidget(painel)

        # ── Rodapé ────────────────────────────────────────────────────────────
        rodape = QLabel("v1.0.0  •  2026")
        rodape.setObjectName("lbl_versao")
        rodape.setAlignment(Qt.AlignCenter)
        rodape.setContentsMargins(0, 8, 0, 12)
        outer.addWidget(rodape)

    def _tentar_login(self):
        """Valida credenciais e emite sinal se correto."""
        usuario = self.campo_usuario.text().strip().lower()
        senha = self.campo_senha.text()

        if not usuario:
            self._mostrar_erro("Informe o nome de usuário.")
            self.campo_usuario.setFocus()
            return

        if not senha:
            self._mostrar_erro("Informe a senha.")
            self.campo_senha.setFocus()
            return

        if _USUARIOS_PADRAO.get(usuario) == senha:
            self.lbl_erro.hide()

            # Persistir usuário se "lembrar" marcado
            if self.chk_lembrar.isChecked():
                self._salvar_usuario(usuario)
            else:
                self._limpar_usuario_salvo()

            self.login_realizado.emit(usuario)
            self.accept()
        else:
            self._mostrar_erro("Usuário ou senha incorretos.")
            self.campo_senha.clear()
            self.campo_senha.setFocus()

    def _mostrar_erro(self, msg: str):
        self.lbl_erro.setText(f"⚠ {msg}")
        self.lbl_erro.show()

    def _salvar_usuario(self, usuario: str):
        """Persiste o nome do usuário na tabela settings."""
        try:
            conn = self._db.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO settings (chave, valor, tipo)
                VALUES ('ultimo_usuario', ?, 'string')
                ON CONFLICT(chave) DO UPDATE SET valor=excluded.valor,
                atualizado_em=CURRENT_TIMESTAMP
            """, (usuario,))
            conn.commit()
            conn.close()
        except Exception:
            pass

    def _limpar_usuario_salvo(self):
        """Remove usuário salvo da tabela settings."""
        try:
            conn = self._db.get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM settings WHERE chave='ultimo_usuario'")
            conn.commit()
            conn.close()
        except Exception:
            pass

    def _carregar_usuario_salvo(self):
        """Pré-preenche o campo usuário se houver salvo."""
        try:
            conn = self._db.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT valor FROM settings WHERE chave='ultimo_usuario'")
            row = cursor.fetchone()
            conn.close()
            if row and row[0]:
                self.campo_usuario.setText(row[0])
                self.chk_lembrar.setChecked(True)
                self.campo_senha.setFocus()
        except Exception:
            pass
