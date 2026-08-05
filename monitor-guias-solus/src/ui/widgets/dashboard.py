from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor
from datetime import datetime

class IndicatorCard(QFrame):
    """Card de indicador no painel"""
    
    def __init__(self, title: str, value: int, icon_text: str = "", color: str = "#0066cc"):
        super().__init__()
        self.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 20px;
            }}
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Ícone e Título
        top_layout = QHBoxLayout()
        
        icon_label = QLabel(icon_text)
        icon_label.setFont(QFont("Arial", 24))
        icon_label.setStyleSheet(f"color: {color};")
        top_layout.addWidget(icon_label)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 11))
        title_label.setStyleSheet("color: #666666;")
        top_layout.addWidget(title_label, 1)
        
        layout.addLayout(top_layout)
        
        # Valor
        value_label = QLabel(str(value))
        value_label.setFont(QFont("Arial", 32, QFont.Bold))
        value_label.setStyleSheet(f"color: {color};")
        layout.addWidget(value_label)
        
        self.setLayout(layout)

class DashboardPanel(QWidget):
    """Painel com indicadores principais"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)
        
        # Título
        title = QLabel("INDICADORES")
        title.setFont(QFont("Arial", 12, QFont.Bold))
        title.setStyleSheet("color: #333333; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Cards em grid horizontal
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(15)
        
        self.card_monitoring = IndicatorCard("Em monitoramento", 32, "📋", "#0066cc")
        self.card_today = IndicatorCard("Atualizadas hoje", 5, "🔔", "#FFA500")
        self.card_pending = IndicatorCard("Pendentes de ciência", 7, "⚠️", "#FF6B6B")
        self.card_errors = IndicatorCard("Erros na consulta", 1, "❌", "#999999")
        
        cards_layout.addWidget(self.card_monitoring)
        cards_layout.addWidget(self.card_today)
        cards_layout.addWidget(self.card_pending)
        cards_layout.addWidget(self.card_errors)
        
        layout.addLayout(cards_layout)
        
        # Espaço em branco
        layout.addStretch()
        
        self.setLayout(layout)
    
    def update_indicators(self, data: dict):
        """Atualiza os indicadores com novos dados"""
        pass
