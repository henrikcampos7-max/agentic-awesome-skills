from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QMessageBox
from PySide6.QtCore import Qt, QTimer, QDate
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
    """Janela principal da aplicaÃ§Ã£o"""
    
    # T28: usuario_logado mantÃ©m o usuÃ¡rio ativo na sessÃ£o
    usuario_logado: str = "phenrique"

    def __init__(self, usuario: str = "phenrique"):
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

        # Timer para sincronizaÃ§Ã£o
        self.sync_timer = QTimer()
        self.sync_timer.timeout.connect(self.sync_guides)
        self.sync_timer.start(60000)  # 60 s para demo; produÃ§Ã£o: 60 min
    
    def init_ui(self):
        """Inicializa a interface"""
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)
        
        # Header
        header_layout = QHBoxLayout()
        header_layout.setSpacing(20)
        
        # TÃ­tulo
        title = QLabel("MONITOR DE GUIAS - SOLUS")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setStyleSheet("color: #1a3a52;")
        header_layout.addWidget(title)
        
        # SincronizaÃ§Ã£o info
        self.sync_label = QLabel("SincronizaÃ§Ã£o: 11:00:00")
        self.sync_label.setFont(QFont("Arial", 10))
        self.sync_label.setStyleSheet("color: #666666;")
        header_layout.addStretch()
        header_layout.addWidget(self.sync_label)
        
        # Status
        status_label = QLabel("ðŸŸ¢ Ativo")
        status_label.setFont(QFont("Arial", 10))
        status_label.setStyleSheet("color: #228B22;")
        header_layout.addWidget(status_label)
        
        # BotÃ£o de sincronizaÃ§Ã£o
        sync_btn = QPushButton("ðŸ”„ Sincronizar agora")
        sync_btn.setMaximumWidth(150)
        sync_btn.clicked.connect(self.sync_guides)
        header_layout.addWidget(sync_btn)
        
        # BotÃ£o de configuraÃ§Ãµes (T26)
        actions_btn = QPushButton("âš™ï¸")
        actions_btn.setMaximumWidth(40)
        actions_btn.setToolTip("ConfiguraÃ§Ãµes")
        actions_btn.clicked.connect(self.abrir_configuracoes)
        header_layout.addWidget(actions_btn)
        
        main_layout.addLayout(header_layout)
        
        # Painel de aÃ§Ãµes
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(10)
        
        nova_guia_btn = QPushButton("âž• Nova Guia")
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

        self._connect_filters()
        
        # T29 â€” Barra de status dinÃ¢mica
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

        # T28: exibe usuÃ¡rio logado dinamicamente
        self.lbl_usuario_status = QLabel(f"ðŸ‘¤ {self.usuario_logado}")
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
        # Implementar lÃ³gica de indicadores
        pass
    
    def sync_guides(self):
        """Sincroniza guias com o Solus."""
        agora = datetime.now().strftime("%H:%M:%S")
        self.sync_label.setText(f"SincronizaÃ§Ã£o: {agora}")
        self.refresh_table()
        QMessageBox.information(self, "Sincronizado", f"Guias sincronizadas com sucesso!\nHorÃ¡rio: {agora}")

    def abrir_configuracoes(self):
        """Abre a tela de configuraÃ§Ãµes (T26)."""
        dialog = ConfiguracoesDialog(self.db, self)
        dialog.configuracoes_salvas.connect(self.refresh_table)
        dialog.exec()
    
    def add_new_guide(self):
        """Abre o dialog de Nova Guia e salva no banco se confirmado."""
        dialog = NovaGuiaDialog(self)
        dialog.guia_adicionada.connect(self._salvar_nova_guia)
        dialog.exec()

    def _salvar_nova_guia(self, numero: str, paciente: str, status: str):
        """Callback do sinal guia_adicionada â€” persiste no banco."""
        if self.db.add_guide(numero, paciente, status):
            self.refresh_table()
            QMessageBox.information(self, "Sucesso", f"Guia {numero} adicionada com sucesso!")
        else:
            QMessageBox.warning(self, "Erro", f"NÃºmero de guia '{numero}' jÃ¡ existe no sistema!")

    def show_historico(self, guide: dict):
        """Abre o dialog de HistÃ³rico / CiÃªncia para a guia informada."""
        historico = self.db.get_history(guide.get("id", -1))
        dialog = HistoricoDialog(guide, historico, self)
        dialog.marcar_ciente.connect(self._marcar_guia_ciente)
        dialog.exec()

    def _marcar_guia_ciente(self, guide_id: int, observacoes: str):
        """Callback do sinal marcar_ciente â€” atualiza ciÃªncia no banco."""
        self.db.mark_as_aware(guide_id)
        self.refresh_table()
        QMessageBox.information(self, "CiÃªncia registrada", "CiÃªncia da guia registrada com sucesso!")

    def _connect_filters(self):
        """Conecta eventos dos filtros."""
        if hasattr(self.filters, "status_combo"):
            self.filters.status_combo.currentIndexChanged.connect(self.apply_filters)

        if hasattr(self.filters, "data_inicio"):
            self.filters.data_inicio.dateChanged.connect(self.apply_filters)
        if hasattr(self.filters, "data_fim"):
            self.filters.data_fim.dateChanged.connect(self.apply_filters)

        if hasattr(self.filters, "chk_atualizadas_hoje"):
            self.filters.chk_atualizadas_hoje.toggled.connect(self.apply_filters)
        if hasattr(self.filters, "chk_pendentes_ciencia"):
            self.filters.chk_pendentes_ciencia.toggled.connect(self.apply_filters)

        if hasattr(self.filters, "btn_limpar"):
            self.filters.btn_limpar.clicked.connect(self._limpar_filtros)

    def _limpar_filtros(self):
        """Reseta filtros e recarrega lista completa."""
        if hasattr(self.filters, "status_combo"):
            self.filters.status_combo.setCurrentIndex(0)

        hoje = QDate.currentDate()
        if hasattr(self.filters, "data_inicio"):
            self.filters.data_inicio.setDate(hoje.addDays(-30))
        if hasattr(self.filters, "data_fim"):
            self.filters.data_fim.setDate(hoje)

        if hasattr(self.filters, "chk_atualizadas_hoje"):
            self.filters.chk_atualizadas_hoje.setChecked(False)
        if hasattr(self.filters, "chk_pendentes_ciencia"):
            self.filters.chk_pendentes_ciencia.setChecked(False)

        self.refresh_table()

    def apply_filters(self):
        """Aplica filtros em memÃ³ria e atualiza tabela."""
        guides = self.db.get_all_guides()

        status_val = ""
        if hasattr(self.filters, "status_combo"):
            status_val = self.filters.status_combo.currentText().strip()

        if status_val and status_val.lower() not in ("todos", "todas", "all"):
            guides = [g for g in guides if (g.get("status") or "").strip() == status_val]

        if hasattr(self.filters, "data_inicio") and hasattr(self.filters, "data_fim"):
            dt_ini = self.filters.data_inicio.date().toPython()
            dt_fim = self.filters.data_fim.date().toPython()

            filtradas = []
            for g in guides:
                ua = g.get("ultima_alteracao")
                if not ua:
                    continue
                try:
                    data = datetime.strptime(str(ua)[:19], "%Y-%m-%d %H:%M:%S").date()
                    if dt_ini <= data <= dt_fim:
                        filtradas.append(g)
                except Exception:
                    filtradas.append(g)
            guides = filtradas

        if hasattr(self.filters, "chk_atualizadas_hoje") and self.filters.chk_atualizadas_hoje.isChecked():
            hoje = datetime.now().date()
            tmp = []
            for g in guides:
                ua = g.get("ultima_alteracao")
                if not ua:
                    continue
                try:
                    data = datetime.strptime(str(ua)[:19], "%Y-%m-%d %H:%M:%S").date()
                    if data == hoje:
                        tmp.append(g)
                except Exception:
                    pass
            guides = tmp

        if hasattr(self.filters, "chk_pendentes_ciencia") and self.filters.chk_pendentes_ciencia.isChecked():
            guides = [g for g in guides if (g.get("ciencia_status") or "").strip().lower() == "pendente"]

        self.table_widget.load_guides(guides)
        self._update_indicators(guides)
        total = len(guides)
        self.lbl_total.setText(f"Exibindo {total} registro{'s' if total != 1 else ''}")
