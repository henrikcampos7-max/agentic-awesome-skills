from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont
from datetime import datetime
from typing import List, Dict, Any

class GuidesTable(QWidget):
    """Tabela de guias com filtros e ações"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Tabela
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "Status",
            "Número da Guia",
            "Nome do Paciente",
            "Status Atual",
            "Última Consulta",
            "Última Alteração",
            "Ciência",
            "Ações"
        ])
        
        # Configurar colunas
        self.table.setColumnWidth(0, 50)   # Status (cor)
        self.table.setColumnWidth(1, 100)  # Número
        self.table.setColumnWidth(2, 200)  # Paciente
        self.table.setColumnWidth(3, 150)  # Status Atual
        self.table.setColumnWidth(4, 150)  # Última Consulta
        self.table.setColumnWidth(5, 150)  # Última Alteração
        self.table.setColumnWidth(6, 100)  # Ciência
        self.table.setColumnWidth(7, 150)  # Ações
        
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                gridline-color: #e0e0e0;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #e6f2ff;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                padding: 5px;
                border: 1px solid #cccccc;
                font-weight: bold;
            }
        """)
        
        layout.addWidget(self.table)
        self.setLayout(layout)
    
    def load_guides(self, guides: List[Dict[str, Any]]):
        """Carrega guias na tabela"""
        self.table.setRowCount(0)
        
        for idx, guide in enumerate(guides):
            self.table.insertRow(idx)
            
            # Status (color indicator)
            status_item = QTableWidgetItem()
            status_color = self._get_status_color(guide.get("status", ""))
            status_item.setBackground(QColor(status_color))
            self.table.setItem(idx, 0, status_item)
            
            # Número da Guia
            numero_item = QTableWidgetItem(str(guide.get("numero_guia", "")))
            numero_item.setFont(QFont("Arial", 10))
            self.table.setItem(idx, 1, numero_item)
            
            # Paciente
            paciente_item = QTableWidgetItem(str(guide.get("paciente", "")))
            paciente_item.setFont(QFont("Arial", 10))
            self.table.setItem(idx, 2, paciente_item)
            
            # Status Atual
            status_atual_item = QTableWidgetItem(str(guide.get("status", "")))
            status_atual_item.setFont(QFont("Arial", 9))
            self.table.setItem(idx, 3, status_atual_item)
            
            # Última Consulta
            ultima_consulta = guide.get("ultima_consulta")
            if ultima_consulta:
                if isinstance(ultima_consulta, datetime):
                    consulta_text = ultima_consulta.strftime("%d/%m/%Y %H:%M")
                else:
                    consulta_text = str(ultima_consulta)
            else:
                consulta_text = "-"
            consulta_item = QTableWidgetItem(consulta_text)
            consulta_item.setFont(QFont("Arial", 9))
            self.table.setItem(idx, 4, consulta_item)
            
            # Última Alteração
            ultima_alter = guide.get("ultima_alteracao")
            if ultima_alter:
                if isinstance(ultima_alter, datetime):
                    alter_text = ultima_alter.strftime("%d/%m/%Y %H:%M")
                else:
                    alter_text = str(ultima_alter)
            else:
                alter_text = "-"
            alter_item = QTableWidgetItem(alter_text)
            alter_item.setFont(QFont("Arial", 9))
            self.table.setItem(idx, 5, alter_item)
            
            # Ciência
            ciencia_status = guide.get("ciencia_status", "Pendente")
            if ciencia_status == "Pendente":
                ciencia_text = "🔴 Pendente"
            else:
                ciencia_text = "🟢 Ciente"
            
            ciencia_item = QTableWidgetItem(ciencia_text)
            ciencia_item.setFont(QFont("Arial", 9))
            self.table.setItem(idx, 6, ciencia_item)
            
            # Ações (botões)
            actions_layout = QHBoxLayout()
            
            historico_btn = QPushButton("👁️ Histórico")
            historico_btn.setMaximumWidth(100)
            historico_btn.setStyleSheet("""
                QPushButton {
                    background-color: #0066cc;
                    color: white;
                    border: none;
                    border-radius: 3px;
                    padding: 4px 8px;
                    font-size: 10px;
                }
                QPushButton:hover {
                    background-color: #0052a3;
                }
            """)
            
            actions_layout.addWidget(historico_btn)
            actions_layout.addStretch()
            
            actions_widget = QWidget()
            actions_widget.setLayout(actions_layout)
            self.table.setCellWidget(idx, 7, actions_widget)
    
    def _get_status_color(self, status: str) -> str:
        """Retorna cor baseado no status"""
        colors = {
            "Guia emitida / liberada": "#FFFFFF",
            "Guia negada": "#FF0000",
            "Guia cancelada": "#FF6B6B",
            "Guia pedido/aguard confirmação": "#FFD700",
            "Guia com setor de OPME": "#9932CC",
            "Sob auditoria na Unimed origem": "#87CEEB",
            "Guia parcialmente liberada": "#FFA500",
            "Cancelada na Unimed origem": "#00CED1",
            "Negada na Unimed origem": "#D3D3D3",
            "Guia sob auditoria": "#228B22"
        }
        return colors.get(status, "#FFFFFF")
