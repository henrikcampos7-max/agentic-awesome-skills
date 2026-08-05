from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QDateEdit, QCheckBox, QPushButton
from PySide6.QtCore import Qt, QDate

class FiltersPanel(QWidget):
    """Painel de filtros"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Título
        title = QLabel("FILTROS")
        title.setStyleSheet("font-weight: bold; font-size: 11px; color: #333333;")
        layout.addWidget(title)
        
        # Primeira linha de filtros
        filters_row1 = QHBoxLayout()
        filters_row1.setSpacing(10)
        
        # Status
        status_label = QLabel("Status:")
        status_label.setStyleSheet("font-size: 10px;")
        self.status_combo = QComboBox()
        self.status_combo.addItems(["Todos", "Guia emitida / liberada", "Guia negada", "Guia cancelada", "Guia sob auditoria"])
        self.status_combo.setMaximumWidth(200)
        filters_row1.addWidget(status_label)
        filters_row1.addWidget(self.status_combo)
        
        # Período
        periodo_label = QLabel("Período:")
        periodo_label.setStyleSheet("font-size: 10px;")
        self.date_from = QDateEdit()
        self.date_from.setDate(QDate.currentDate().addDays(-30))
        self.date_from.setMaximumWidth(100)
        self.date_to = QDateEdit()
        self.date_to.setDate(QDate.currentDate())
        self.date_to.setMaximumWidth(100)
        
        filters_row1.addWidget(periodo_label)
        filters_row1.addWidget(self.date_from)
        filters_row1.addWidget(QLabel("até"))
        filters_row1.addWidget(self.date_to)
        
        layout.addLayout(filters_row1)
        
        # Segunda linha de filtros (checkboxes)
        filters_row2 = QHBoxLayout()
        filters_row2.setSpacing(20)
        
        self.today_checkbox = QCheckBox("Somente atualizadas hoje")
        self.today_checkbox.setStyleSheet("font-size: 10px;")
        filters_row2.addWidget(self.today_checkbox)
        
        self.pending_checkbox = QCheckBox("Somente pendentes de ciência")
        self.pending_checkbox.setStyleSheet("font-size: 10px;")
        filters_row2.addWidget(self.pending_checkbox)
        
        # Botão Limpar Filtros
        clear_btn = QPushButton("🔄 Limpar filtros")
        clear_btn.setMaximumWidth(120)
        filters_row2.addWidget(clear_btn)
        
        filters_row2.addStretch()
        
        layout.addLayout(filters_row2)
        layout.addSpacing(10)
        
        self.setLayout(layout)
