from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QMessageBox
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
from datetime import datetime
from src.database.schema import Database
from src.adapters.simulator import SimulatedSolusAdapter
from src.ui.widgets.dashboard import DashboardPanel
from src.ui.widgets.table import GuidesTable
from src.ui.widgets.filters import FiltersPanel
from src.ui.widgets.dialogs import NovaGuiaDialog, HistoricoDialog
from src.ui.configuracoes import ConfiguracoesDialog
from src.ui.styles.stylesheet import STYLESHEET

VERSAO = "1.1.0"

class MainWindow(QMainWindow):
    """Janela principal da aplicação"""
    
    # T28: usuario_logado mantém o usuário ativo na sessão
    usuario_logado: str = "henrique.campos"

    def __init__(self, usuario: str = "henrique.campos"):
        super().__init__()
        self.usuario_logado = usuario
        self.setWindowTitle("Monitor de Guias - Solus")
        self.setGeometry(100, 100, 1400, 800)

        # Database
        self.db = Database()

        # Adapter simulado
        self.adapter = SimulatedSolusAdapter()

        # Inicializar dados simulados no banco
        self._load_simulated_data()

        # UI
        self.init_ui()

        # Timer para sincronização
        self.sync_timer = QTimer()
        self.sync_timer.timeout.connect(self.sync_guides)
        self.sync_timer.start(60000)  # 60 s para demo; produção: 60 min
    
    def init_ui(self):
        """Inicializa a interface"""
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)
        
        # Header
        header_layout = QHBoxLayout()
        header_layout.setSpacing(20)
        
        # Título
        title = QLabel("MONITOR DE GUIAS - SOLUS")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setStyleSheet("color: #1a3a52;")
        header_layout.addWidget(title)
        
        # Sincronização info
        self.sync_label = QLabel("Sincronização: 11:00:00")
        self.sync_label.setFont(QFont("Arial", 10))
        self.sync_label.setStyleSheet("color: #666666;")
        header_layout.addStretch()
        header_layout.addWidget(self.sync_label)
        
        # Status
        status_label = QLabel("🟢 Ativo")
        status_label.setFont(QFont("Arial", 10))
        status_label.setStyleSheet("color: #228B22;")
        header_layout.addWidget(status_label)
        
        # Botão de sincronização
        sync_btn = QPushButton("🔄 Sincronizar agora")
        sync_btn.setMaximumWidth(150)
        sync_btn.clicked.connect(self.sync_guides)
        header_layout.addWidget(sync_btn)
        
        # Botão de configurações (T26)
        actions_btn = QPushButton("⚙️")
        actions_btn.setMaximumWidth(40)
        actions_btn.setToolTip("Configurações")
        actions_btn.clicked.connect(self.abrir_configuracoes)
        header_layout.addWidget(actions_btn)
        
        main_layout.addLayout(header_layout)
        
        # Painel de ações
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(10)
        
        nova_guia_btn = QPushButton("➕ Nova Guia")
        nova_guia_btn.setMaximumWidth(150)
        nova_guia_btn.clicked.connect(self.add_new_guide)
        actions_layout.addWidget(nova_guia_btn)
        
        actions_layout.addStretch()
        
        main_layout.addLayout(actions_layout)
        
        # Dashboard
        self.dashboard = DashboardPanel()
        main_layout.addWidget(self.dashboard)
        
        # Filtros
        self.filters = FiltersPanel()
        main_layout.addWidget(self.filters)
        
        # Tabela
        self.table_widget = GuidesTable()
        main_layout.addWidget(self.table_widget)
        
        # T29 — Barra de status dinâmica
        footer_layout = QHBoxLayout()
        sep_footer = QLabel()
        sep_footer.setFixedHeight(1)
        sep_footer.setStyleSheet("background: #dddddd;")
        main_layout.addWidget(sep_footer)

        self.lbl_total = QLabel("Exibindo 0 registros")
        self.lbl_total.setFont(QFont("Arial", 9))
        self.lbl_total.setStyleSheet("color: #666666;")
        footer_layout.addWidget(self.lbl_total)
        footer_layout.addStretch()

        # T28: exibe usuário logado dinamicamente
        self.lbl_usuario_status = QLabel(f"👤 {self.usuario_logado}")
        self.lbl_usuario_status.setFont(QFont("Arial", 9))
        self.lbl_usuario_status.setStyleSheet("color: #444444;")
        footer_layout.addWidget(self.lbl_usuario_status)

        self.lbl_versao_status = QLabel(f"  v{VERSAO}")
        self.lbl_versao_status.setFont(QFont("Arial", 9))
        self.lbl_versao_status.setStyleSheet("color: #888888;")
        footer_layout.addWidget(self.lbl_versao_status)

        main_layout.addLayout(footer_layout)
        
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        # Aplicar stylesheet
        self.setStyleSheet(STYLESHEET)
        
        # Carregar dados
        self.refresh_table()
    
    def _load_simulated_data(self):
        """Carrega dados simulados no banco"""
        guides = self.adapter.get_guides()
        for guide in guides:
            self.db.add_guide(
                guide["numero_guia"],
                guide["paciente"],
                guide["status"]
            )
    
    def refresh_table(self):
        """Atualiza a tabela, indicadores e barra de status."""
        guides = self.db.get_all_guides()
        self.table_widget.load_guides(guides)
        self._update_indicators(guides)
        # T29: atualizar contador na barra de status
        total = len(guides)
        self.lbl_total.setText(f"Exibindo {total} registro{'s' if total != 1 else ''}")
    
    def _update_indicators(self, guides: list):
        """Atualiza os indicadores do painel"""
        # Implementar lógica de indicadores
        pass
    
    def sync_guides(self):
        """Sincroniza guias com o Solus."""
        agora = datetime.now().strftime("%H:%M:%S")
        self.sync_label.setText(f"Sincronização: {agora}")
        self.refresh_table()
        QMessageBox.information(self, "Sincronizado", f"Guias sincronizadas com sucesso!\nHorário: {agora}")

    def abrir_configuracoes(self):
        """Abre a tela de configurações (T26)."""
        dialog = ConfiguracoesDialog(self.db, self)
        dialog.configuracoes_salvas.connect(self.refresh_table)
        dialog.exec()
    
    def add_new_guide(self):
        """Abre o dialog de Nova Guia e salva no banco se confirmado."""
        dialog = NovaGuiaDialog(self)
        dialog.guia_adicionada.connect(self._salvar_nova_guia)
        dialog.exec()

    def _salvar_nova_guia(self, numero: str, paciente: str, status: str):
        """Callback do sinal guia_adicionada — persiste no banco."""
        if self.db.add_guide(numero, paciente, status):
            self.refresh_table()
            QMessageBox.information(self, "Sucesso", f"Guia {numero} adicionada com sucesso!")
        else:
            QMessageBox.warning(self, "Erro", f"Número de guia '{numero}' já existe no sistema!")

    def show_historico(self, guide: dict):
        """Abre o dialog de Histórico / Ciência para a guia informada."""
        historico = self.db.get_history(guide.get("id", -1))
        dialog = HistoricoDialog(guide, historico, self)
        dialog.marcar_ciente.connect(self._marcar_guia_ciente)
        dialog.exec()

    def _marcar_guia_ciente(self, guide_id: int, observacoes: str):
        """Callback do sinal marcar_ciente — atualiza ciência no banco."""
        self.db.mark_as_aware(guide_id)
        self.refresh_table()
        QMessageBox.information(self, "Ciência registrada", "Ciência da guia registrada com sucesso!")
