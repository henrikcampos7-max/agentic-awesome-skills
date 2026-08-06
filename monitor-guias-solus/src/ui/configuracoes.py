"""
T26 — Tela de Configurações
Permite configurar: intervalo de sync, credenciais Solus, notificações e dados do usuário.
Persiste todas as preferências na tabela settings do SQLite.
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QLineEdit, QPushButton, QCheckBox,
    QSpinBox, QGroupBox, QFrame, QMessageBox
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from src.database.schema import Database

_CONFIG_STYLE = """
QDialog {
    background-color: #f5f5f5;
}
QLabel {
    color: #333333;
    font-size: 13px;
}
QLabel#titulo {
    color: #1a3a52;
    font-size: 16px;
    font-weight: bold;
}
QGroupBox {
    border: 1px solid #d0d0d0;
    border-radius: 6px;
    margin-top: 12px;
    padding-top: 10px;
    font-weight: bold;
    font-size: 12px;
    color: #1a3a52;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 4px;
}
QLineEdit, QSpinBox {
    border: 1px solid #cccccc;
    border-radius: 4px;
    padding: 8px;
    background-color: white;
    color: #333333;
    font-size: 13px;
    min-height: 20px;
}
QLineEdit:focus, QSpinBox:focus {
    border: 2px solid #0066cc;
}
QPushButton#btn_salvar {
    background-color: #0066cc;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 10px 24px;
    font-weight: bold;
    font-size: 13px;
}
QPushButton#btn_salvar:hover { background-color: #0052a3; }
QPushButton#btn_cancelar {
    background-color: #e0e0e0;
    color: #333333;
    border: none;
    border-radius: 4px;
    padding: 10px 24px;
    font-size: 13px;
}
QPushButton#btn_cancelar:hover { background-color: #cccccc; }
QCheckBox { color: #444444; font-size: 12px; spacing: 6px; }
QFrame#sep { background-color: #dddddd; max-height: 1px; }
"""

# Chaves usadas na tabela settings
_CHAVES = {
    "intervalo_sync": ("60", "int"),
    "solus_url": ("", "string"),
    "solus_login": ("", "string"),
    "solus_senha": ("", "string"),
    "notif_mudanca": ("1", "bool"),
    "notif_negada": ("1", "bool"),
    "notif_aprovada": ("0", "bool"),
    "usuario_nome": ("", "string"),
    "usuario_unidade": ("Farmácia Oncológica Cacoal", "string"),
}


class ConfiguracoesDialog(QDialog):
    """
    Tela de configurações do sistema.

    Permite ajustar sincronização, credenciais Solus, notificações e dados do usuário.
    Todos os valores são lidos e gravados na tabela `settings` do SQLite.

    Emite:
        configuracoes_salvas: () após salvar com sucesso
    """

    configuracoes_salvas = Signal()

    def __init__(self, db: Database, parent=None):
        super().__init__(parent)
        self._db = db
        self.setWindowTitle("⚙️ Configurações")
        self.setMinimumWidth(500)
        self.setModal(True)
        self.setStyleSheet(_CONFIG_STYLE)
        self._campos: dict = {}
        self._build_ui()
        self._carregar()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(14)

        # Título
        titulo = QLabel("⚙️ Configurações do Sistema")
        titulo.setObjectName("titulo")
        layout.addWidget(titulo)

        sep = QFrame()
        sep.setObjectName("sep")
        sep.setFrameShape(QFrame.HLine)
        layout.addWidget(sep)

        # ── Grupo: Sincronização ──────────────────────────────────────────────
        grp_sync = QGroupBox("🔄 Sincronização")
        form_sync = QFormLayout(grp_sync)
        form_sync.setSpacing(10)
        form_sync.setLabelAlignment(Qt.AlignRight)

        self._campos["intervalo_sync"] = QSpinBox()
        self._campos["intervalo_sync"].setRange(5, 1440)
        self._campos["intervalo_sync"].setSuffix("  minutos")
        form_sync.addRow("Intervalo:", self._campos["intervalo_sync"])

        self._campos["solus_url"] = QLineEdit()
        self._campos["solus_url"].setPlaceholderText("https://solus.unimed.coop.br/...")
        form_sync.addRow("URL do Solus:", self._campos["solus_url"])

        self._campos["solus_login"] = QLineEdit()
        self._campos["solus_login"].setPlaceholderText("usuario.solus")
        form_sync.addRow("Login Solus:", self._campos["solus_login"])

        self._campos["solus_senha"] = QLineEdit()
        self._campos["solus_senha"].setEchoMode(QLineEdit.Password)
        self._campos["solus_senha"].setPlaceholderText("••••••••")
        form_sync.addRow("Senha Solus:", self._campos["solus_senha"])

        layout.addWidget(grp_sync)

        # ── Grupo: Notificações ───────────────────────────────────────────────
        grp_notif = QGroupBox("🔔 Notificações Windows")
        notif_layout = QVBoxLayout(grp_notif)
        notif_layout.setSpacing(8)

        self._campos["notif_mudanca"] = QCheckBox("Notificar qualquer mudança de status")
        self._campos["notif_negada"] = QCheckBox("Notificar guias negadas")
        self._campos["notif_aprovada"] = QCheckBox("Notificar guias aprovadas/liberadas")

        notif_layout.addWidget(self._campos["notif_mudanca"])
        notif_layout.addWidget(self._campos["notif_negada"])
        notif_layout.addWidget(self._campos["notif_aprovada"])

        layout.addWidget(grp_notif)

        # ── Grupo: Usuário ────────────────────────────────────────────────────
        grp_user = QGroupBox("👤 Identificação do Usuário")
        form_user = QFormLayout(grp_user)
        form_user.setSpacing(10)
        form_user.setLabelAlignment(Qt.AlignRight)

        self._campos["usuario_nome"] = QLineEdit()
        self._campos["usuario_nome"].setPlaceholderText("henrique.campos")
        form_user.addRow("Nome / Login:", self._campos["usuario_nome"])

        self._campos["usuario_unidade"] = QLineEdit()
        self._campos["usuario_unidade"].setPlaceholderText("Farmácia Oncológica Cacoal")
        form_user.addRow("Unidade:", self._campos["usuario_unidade"])

        layout.addWidget(grp_user)

        layout.addStretch()

        # Botões
        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)
        btn_row.addStretch()

        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setObjectName("btn_cancelar")
        btn_cancelar.setMinimumWidth(100)
        btn_cancelar.clicked.connect(self.reject)
        btn_row.addWidget(btn_cancelar)

        btn_salvar = QPushButton("💾 Salvar")
        btn_salvar.setObjectName("btn_salvar")
        btn_salvar.setMinimumWidth(120)
        btn_salvar.setDefault(True)
        btn_salvar.clicked.connect(self._salvar)
        btn_row.addWidget(btn_salvar)

        layout.addLayout(btn_row)

    def _carregar(self):
        """Carrega valores persistidos do banco para os campos."""
        try:
            conn = self._db.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT chave, valor FROM settings")
            rows = {r["chave"]: r["valor"] for r in cursor.fetchall()}
            conn.close()
        except Exception:
            rows = {}

        # Defaults
        for chave, (padrao, _) in _CHAVES.items():
            valor = rows.get(chave, padrao)
            campo = self._campos.get(chave)
            if campo is None:
                continue
            if isinstance(campo, QSpinBox):
                campo.setValue(int(valor) if valor else 60)
            elif isinstance(campo, QCheckBox):
                campo.setChecked(valor == "1")
            elif isinstance(campo, QLineEdit):
                campo.setText(valor or "")

    def _salvar(self):
        """Persiste todos os campos na tabela settings e emite sinal."""
        try:
            conn = self._db.get_connection()
            cursor = conn.cursor()

            for chave, (_, tipo) in _CHAVES.items():
                campo = self._campos.get(chave)
                if campo is None:
                    continue
                if isinstance(campo, QSpinBox):
                    valor = str(campo.value())
                elif isinstance(campo, QCheckBox):
                    valor = "1" if campo.isChecked() else "0"
                else:
                    valor = campo.text().strip()

                cursor.execute("""
                    INSERT INTO settings (chave, valor, tipo)
                    VALUES (?, ?, ?)
                    ON CONFLICT(chave) DO UPDATE
                    SET valor=excluded.valor, atualizado_em=CURRENT_TIMESTAMP
                """, (chave, valor, tipo))

            conn.commit()
            conn.close()

            self.configuracoes_salvas.emit()
            QMessageBox.information(self, "Salvo", "Configurações salvas com sucesso!")
            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao salvar configurações:\n{e}")
