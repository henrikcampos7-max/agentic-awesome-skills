from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QInputDialog, QMessageBox
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
from datetime import datetime
from src.database.schema import Database
from src.adapters.simulator import SimulatedSolusAdapter
from src.ui.widgets.dashboard import DashboardPanel
from src.ui.widgets.table import GuidesTable
from src.ui.widgets.filters import FiltersPanel
from src.ui.styles.stylesheet import STYLESHEET

class MainWindow(QMainWindow):
    """Janela principal da aplicação"""
    
    def __init__(self):
        super().__init__()
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
        self.sync_timer.start(60000)  # 60 segundos para demo (será 60 minutos em produção)
    
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
        
        # Botão de ações
        actions_btn = QPushButton("⚙️")
        actions_btn.setMaximumWidth(40)
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
        
        # Footer
        footer_layout = QHBoxLayout()
        footer_label = QLabel("Exibindo 1 a 10 de 32 registros")
        footer_label.setFont(QFont("Arial", 9))
        footer_label.setStyleSheet("color: #666666;")
        footer_layout.addWidget(footer_label)
        footer_layout.addStretch()
        
        user_label = QLabel("Usuário: henrique.campos")
        user_label.setFont(QFont("Arial", 9))
        user_label.setStyleSheet("color: #666666;")
        footer_layout.addWidget(user_label)
        
        version_label = QLabel("Versão: 1.0.0")
        version_label.setFont(QFont("Arial", 9))
        version_label.setStyleSheet("color: #666666;")
        footer_layout.addWidget(version_label)
        
        backup_label = QLabel("Último backup: 05/08/2026 10:30")
        backup_label.setFont(QFont("Arial", 9))
        backup_label.setStyleSheet("color: #666666;")
        footer_layout.addWidget(backup_label)
        
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
        """Atualiza a tabela com dados do banco"""
        guides = self.db.get_all_guides()
        self.table_widget.load_guides(guides)
        
        # Atualizar indicadores
        self._update_indicators(guides)
    
    def _update_indicators(self, guides: list):
        """Atualiza os indicadores do painel"""
        # Implementar lógica de indicadores
        pass
    
    def sync_guides(self):
        """Sincroniza guias com o Solus"""
        self.sync_label.setText(f"Sincronização: {datetime.now().strftime('%H:%M:%S')}")
        self.refresh_table()
        QMessageBox.information(self, "Sucesso", "Guias sincronizadas com sucesso!")
    
    def add_new_guide(self):
        """Adiciona nova guia"""
        numero, ok = QInputDialog.getText(self, "Nova Guia", "Número da Guia:")
        if ok and numero:
            paciente, ok2 = QInputDialog.getText(self, "Nova Guia", "Nome do Paciente:")
            if ok2 and paciente:
                if self.db.add_guide(numero, paciente):
                    self.refresh_table()
                    QMessageBox.information(self, "Sucesso", "Guia adicionada com sucesso!")
                else:
                    QMessageBox.warning(self, "Erro", "Número de guia já existe!")
