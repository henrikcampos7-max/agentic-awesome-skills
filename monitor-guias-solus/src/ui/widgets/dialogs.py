"""
Dialogs do Monitor de Guias Solus

T24: NovaGuiaDialog   — Dialog para adicionar nova guia
T25: HistoricoDialog  — Dialog de histórico e ciência da guia
"""

from typing import Optional, List, Dict, Any

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QLineEdit, QComboBox, QPushButton, QTextEdit,
    QScrollArea, QWidget, QFrame, QMessageBox, QSizePolicy
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QColor

from src.utils.constants import STATUSES, STATUS_COLORS


# ─────────────────────────────────────────────────────────────────────────────
# Estilos internos dos Dialogs
# ─────────────────────────────────────────────────────────────────────────────

_DIALOG_STYLE = """
QDialog {
    background-color: #f5f5f5;
}
QLabel {
    color: #333333;
    font-size: 13px;
}
QLabel#titulo {
    color: #1a3a52;
    font-size: 15px;
    font-weight: bold;
}
QLabel#subtitulo {
    color: #555555;
    font-size: 12px;
}
QLabel#status_badge {
    border-radius: 4px;
    padding: 4px 10px;
    font-size: 11px;
    font-weight: bold;
}
QLineEdit, QComboBox {
    border: 1px solid #cccccc;
    border-radius: 4px;
    padding: 8px;
    background-color: white;
    color: #333333;
    font-size: 13px;
    min-height: 20px;
}
QLineEdit:focus, QComboBox:focus {
    border: 2px solid #0066cc;
}
QTextEdit {
    border: 1px solid #cccccc;
    border-radius: 4px;
    padding: 6px;
    background-color: white;
    color: #333333;
    font-size: 12px;
}
QPushButton {
    border: none;
    border-radius: 4px;
    padding: 9px 20px;
    font-weight: bold;
    font-size: 13px;
}
QPushButton#btn_primario {
    background-color: #0066cc;
    color: white;
}
QPushButton#btn_primario:hover {
    background-color: #0052a3;
}
QPushButton#btn_primario:pressed {
    background-color: #003d7a;
}
QPushButton#btn_ciente {
    background-color: #228B22;
    color: white;
}
QPushButton#btn_ciente:hover {
    background-color: #1a6b1a;
}
QPushButton#btn_cancelar {
    background-color: #e0e0e0;
    color: #333333;
}
QPushButton#btn_cancelar:hover {
    background-color: #cccccc;
}
QFrame#separador {
    background-color: #dddddd;
    max-height: 1px;
}
QFrame#card_historico {
    background-color: white;
    border: 1px solid #e0e0e0;
    border-radius: 6px;
    padding: 8px;
}
"""


# ─────────────────────────────────────────────────────────────────────────────
# T24 — Dialog Nova Guia
# ─────────────────────────────────────────────────────────────────────────────

class NovaGuiaDialog(QDialog):
    """
    Dialog para adicionar uma nova guia ao sistema.

    Campos:
        - Número da Guia (obrigatório, único)
        - Nome do Paciente (obrigatório)
        - Status Inicial (combobox com todos os status possíveis)

    Emite:
        guia_adicionada: (numero_guia, paciente, status) após confirmação válida
    """

    guia_adicionada = Signal(str, str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Adicionar Nova Guia")
        self.setMinimumWidth(420)
        self.setModal(True)
        self.setStyleSheet(_DIALOG_STYLE)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(16)

        # Título
        titulo = QLabel("➕ Adicionar Nova Guia")
        titulo.setObjectName("titulo")
        layout.addWidget(titulo)

        sep = QFrame()
        sep.setObjectName("separador")
        sep.setFrameShape(QFrame.HLine)
        layout.addWidget(sep)

        # Formulário
        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignRight)
        form.setSpacing(12)

        lbl_numero = QLabel("Número da Guia *")
        lbl_numero.setFont(QFont("Arial", 12))
        self.campo_numero = QLineEdit()
        self.campo_numero.setPlaceholderText("Ex: 11624001")
        self.campo_numero.setMaxLength(30)
        form.addRow(lbl_numero, self.campo_numero)

        lbl_paciente = QLabel("Nome do Paciente *")
        lbl_paciente.setFont(QFont("Arial", 12))
        self.campo_paciente = QLineEdit()
        self.campo_paciente.setPlaceholderText("Ex: PEDRO HENRIQUE DA SILVA")
        self.campo_paciente.setMaxLength(120)
        form.addRow(lbl_paciente, self.campo_paciente)

        lbl_status = QLabel("Status Inicial")
        lbl_status.setFont(QFont("Arial", 12))
        self.combo_status = QComboBox()
        for s in STATUSES:
            self.combo_status.addItem(s)
        form.addRow(lbl_status, self.combo_status)

        layout.addLayout(form)

        # Label de erro (oculta por padrão)
        self.lbl_erro = QLabel("")
        self.lbl_erro.setStyleSheet("color: #cc0000; font-size: 12px;")
        self.lbl_erro.setWordWrap(True)
        self.lbl_erro.hide()
        layout.addWidget(self.lbl_erro)

        layout.addStretch()

        # Botões
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        btn_layout.addStretch()

        self.btn_cancelar = QPushButton("Cancelar")
        self.btn_cancelar.setObjectName("btn_cancelar")
        self.btn_cancelar.setMinimumWidth(100)
        self.btn_cancelar.clicked.connect(self.reject)
        btn_layout.addWidget(self.btn_cancelar)

        self.btn_adicionar = QPushButton("✓ Adicionar")
        self.btn_adicionar.setObjectName("btn_primario")
        self.btn_adicionar.setMinimumWidth(120)
        self.btn_adicionar.setDefault(True)
        self.btn_adicionar.clicked.connect(self._confirmar)
        btn_layout.addWidget(self.btn_adicionar)

        layout.addLayout(btn_layout)

    def _confirmar(self):
        """Valida campos e emite sinal se tudo OK."""
        numero = self.campo_numero.text().strip()
        paciente = self.campo_paciente.text().strip().upper()
        status = self.combo_status.currentText()

        # Validação
        if not numero:
            self._mostrar_erro("O número da guia é obrigatório.")
            self.campo_numero.setFocus()
            return

        if not paciente:
            self._mostrar_erro("O nome do paciente é obrigatório.")
            self.campo_paciente.setFocus()
            return

        self.lbl_erro.hide()
        self.guia_adicionada.emit(numero, paciente, status)
        self.accept()

    def _mostrar_erro(self, mensagem: str):
        self.lbl_erro.setText(f"⚠ {mensagem}")
        self.lbl_erro.show()

    def obter_dados(self) -> Dict[str, str]:
        """Retorna os dados preenchidos no formulário."""
        return {
            "numero_guia": self.campo_numero.text().strip(),
            "paciente": self.campo_paciente.text().strip().upper(),
            "status": self.combo_status.currentText(),
        }


# ─────────────────────────────────────────────────────────────────────────────
# T25 — Dialog de Histórico e Ciência
# ─────────────────────────────────────────────────────────────────────────────

class _CardHistorico(QFrame):
    """Card visual para exibir uma entrada do histórico."""

    def __init__(self, entrada: Dict[str, Any], parent=None):
        super().__init__(parent)
        self.setObjectName("card_historico")
        self.setFrameShape(QFrame.StyledPanel)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(4)

        # Linha 1: timestamp + usuário
        timestamp = entrada.get("timestamp", "")
        if hasattr(timestamp, "strftime"):
            timestamp = timestamp.strftime("%d/%m/%y %H:%M")
        else:
            timestamp = str(timestamp)[:16].replace("T", " ")

        usuario = entrada.get("usuario", "Sistema")
        lbl_cabecalho = QLabel(f"🕐 {timestamp}  •  por: {usuario}")
        lbl_cabecalho.setStyleSheet("color: #777777; font-size: 11px;")
        layout.addWidget(lbl_cabecalho)

        # Linha 2: mudança de status
        status_novo = entrada.get("status_novo", "—")
        status_ant = entrada.get("status_anterior", None)

        if status_ant:
            lbl_mudanca = QLabel(
                f"<b>{status_ant}</b>  →  <b style='color:#0066cc'>{status_novo}</b>"
            )
        else:
            lbl_mudanca = QLabel(f"<b style='color:#228B22'>✦ Criação:</b> {status_novo}")

        lbl_mudanca.setTextFormat(Qt.RichText)
        lbl_mudanca.setStyleSheet("font-size: 12px;")
        lbl_mudanca.setWordWrap(True)
        layout.addWidget(lbl_mudanca)

        # Observações (se houver)
        obs = entrada.get("observacoes", "")
        if obs:
            lbl_obs = QLabel(f"Obs: {obs}")
            lbl_obs.setStyleSheet("color: #555555; font-size: 11px; font-style: italic;")
            lbl_obs.setWordWrap(True)
            layout.addWidget(lbl_obs)


class HistoricoDialog(QDialog):
    """
    Dialog de histórico e ciência de uma guia.

    Exibe:
        - Dados da guia (número, paciente, status atual, ciência)
        - Timeline de mudanças de status
        - Campo de observações
        - Botão para marcar como Ciente

    Emite:
        marcar_ciente: (guide_id, observacoes) quando o usuário confirma ciência
    """

    marcar_ciente = Signal(int, str)

    def __init__(
        self,
        guide: Dict[str, Any],
        historico: List[Dict[str, Any]],
        parent=None
    ):
        super().__init__(parent)
        self._guide = guide
        self._historico = historico

        self.setWindowTitle(f"Histórico — Guia {guide.get('numero_guia', '')}")
        self.setMinimumWidth(520)
        self.setMinimumHeight(520)
        self.setModal(True)
        self.setStyleSheet(_DIALOG_STYLE)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(14)

        # ── Cabeçalho ────────────────────────────────────────────────────────
        titulo = QLabel(f"👁  Histórico — Guia {self._guide.get('numero_guia', '')}")
        titulo.setObjectName("titulo")
        layout.addWidget(titulo)

        lbl_paciente = QLabel(f"Paciente: {self._guide.get('paciente', '—')}")
        lbl_paciente.setObjectName("subtitulo")
        layout.addWidget(lbl_paciente)

        sep1 = QFrame()
        sep1.setObjectName("separador")
        sep1.setFrameShape(QFrame.HLine)
        layout.addWidget(sep1)

        # ── Status atual + ciência ────────────────────────────────────────────
        info_layout = QHBoxLayout()
        info_layout.setSpacing(16)

        status_atual = self._guide.get("status", "—")
        cor_hex = STATUS_COLORS.get(status_atual, "#cccccc")
        lbl_status = QLabel(f"Status: {status_atual}")
        lbl_status.setObjectName("status_badge")
        lbl_status.setStyleSheet(
            f"QLabel#status_badge {{ background-color: {cor_hex}; "
            f"color: {'#ffffff' if self._eh_cor_escura(cor_hex) else '#222222'}; "
            f"border-radius: 4px; padding: 4px 10px; font-size: 11px; font-weight: bold; }}"
        )
        lbl_status.setWordWrap(True)
        info_layout.addWidget(lbl_status)

        ciencia = self._guide.get("ciencia_status", "Pendente")
        icone_ciencia = "🟢" if ciencia == "Ciente" else "🔴"
        lbl_ciencia = QLabel(f"{icone_ciencia} Ciência: {ciencia}")
        lbl_ciencia.setStyleSheet(
            "font-size: 12px; font-weight: bold; color: "
            + ("#228B22" if ciencia == "Ciente" else "#cc0000") + ";"
        )
        info_layout.addWidget(lbl_ciencia)
        info_layout.addStretch()

        layout.addLayout(info_layout)

        sep2 = QFrame()
        sep2.setObjectName("separador")
        sep2.setFrameShape(QFrame.HLine)
        layout.addWidget(sep2)

        # ── Timeline de histórico ─────────────────────────────────────────────
        lbl_hist_titulo = QLabel("📋 Histórico de Alterações")
        lbl_hist_titulo.setFont(QFont("Arial", 12, QFont.Bold))
        lbl_hist_titulo.setStyleSheet("color: #1a3a52;")
        layout.addWidget(lbl_hist_titulo)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setMinimumHeight(180)

        conteudo = QWidget()
        conteudo_layout = QVBoxLayout(conteudo)
        conteudo_layout.setContentsMargins(0, 0, 6, 0)
        conteudo_layout.setSpacing(8)

        if self._historico:
            for entrada in self._historico:
                card = _CardHistorico(entrada)
                conteudo_layout.addWidget(card)
        else:
            lbl_vazio = QLabel("Nenhuma alteração registrada.")
            lbl_vazio.setStyleSheet("color: #999999; font-style: italic; font-size: 12px;")
            lbl_vazio.setAlignment(Qt.AlignCenter)
            conteudo_layout.addWidget(lbl_vazio)

        conteudo_layout.addStretch()
        scroll.setWidget(conteudo)
        layout.addWidget(scroll)

        sep3 = QFrame()
        sep3.setObjectName("separador")
        sep3.setFrameShape(QFrame.HLine)
        layout.addWidget(sep3)

        # ── Observações + Botão Ciente ────────────────────────────────────────
        lbl_obs = QLabel("Observações (opcional):")
        lbl_obs.setFont(QFont("Arial", 11))
        layout.addWidget(lbl_obs)

        self.campo_obs = QTextEdit()
        self.campo_obs.setPlaceholderText("Registre aqui o motivo da ciência ou observações relevantes...")
        self.campo_obs.setMaximumHeight(70)
        layout.addWidget(self.campo_obs)

        # Botões
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        btn_layout.addStretch()

        btn_fechar = QPushButton("Fechar")
        btn_fechar.setObjectName("btn_cancelar")
        btn_fechar.setMinimumWidth(100)
        btn_fechar.clicked.connect(self.reject)
        btn_layout.addWidget(btn_fechar)

        # Botão Ciente (desabilitado se já estiver ciente)
        ja_ciente = ciencia == "Ciente"
        self.btn_ciente = QPushButton(
            "✓ Marcar como Ciente" if not ja_ciente else "✔ Já Ciente"
        )
        self.btn_ciente.setObjectName("btn_ciente")
        self.btn_ciente.setMinimumWidth(160)
        self.btn_ciente.setEnabled(not ja_ciente)
        self.btn_ciente.clicked.connect(self._confirmar_ciencia)
        btn_layout.addWidget(self.btn_ciente)

        layout.addLayout(btn_layout)

    def _confirmar_ciencia(self):
        """Emite sinal de ciência com observações e fecha o dialog."""
        guide_id = self._guide.get("id")
        observacoes = self.campo_obs.toPlainText().strip()

        resposta = QMessageBox.question(
            self,
            "Confirmar Ciência",
            f"Confirmar ciência da guia {self._guide.get('numero_guia', '')}?\n\n"
            "Essa ação ficará registrada no histórico de auditoria.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if resposta == QMessageBox.Yes:
            self.marcar_ciente.emit(guide_id, observacoes)
            self.accept()

    @staticmethod
    def _eh_cor_escura(hex_color: str) -> bool:
        """Retorna True se a cor for escura (para usar texto branco)."""
        try:
            hex_color = hex_color.lstrip("#")
            r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
            luminancia = (0.299 * r + 0.587 * g + 0.114 * b)
            return luminancia < 128
        except Exception:
            return False
