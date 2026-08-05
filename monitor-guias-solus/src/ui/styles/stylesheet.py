"""
Stylesheet para a aplicação
"""

STYLESHEET = """
QMainWindow {
    background-color: #f5f5f5;
}

QWidget {
    background-color: #f5f5f5;
    color: #333333;
}

QPushButton {
    background-color: #0066cc;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 8px 16px;
    font-weight: bold;
    font-size: 12px;
}

QPushButton:hover {
    background-color: #0052a3;
}

QPushButton:pressed {
    background-color: #003d7a;
}

QLineEdit, QComboBox {
    border: 1px solid #cccccc;
    border-radius: 4px;
    padding: 8px;
    background-color: white;
    color: #333333;
}

QLineEdit:focus, QComboBox:focus {
    border: 2px solid #0066cc;
}

QTableWidget {
    background-color: white;
    gridline-color: #e0e0e0;
    border: 1px solid #cccccc;
}

QTableWidget::item {
    padding: 5px;
    border: none;
}

QTableWidget::item:selected {
    background-color: #e6f2ff;
}

QHeaderView::section {
    background-color: #f0f0f0;
    padding: 5px;
    border: 1px solid #cccccc;
    font-weight: bold;
    color: #333333;
}

QLabel {
    color: #333333;
}

QGroupBox {
    border: 1px solid #cccccc;
    border-radius: 4px;
    margin-top: 10px;
    padding-top: 10px;
    color: #333333;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 3px 0 3px;
}

QCheckBox {
    spacing: 5px;
    color: #333333;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
}

QScrollBar:vertical {
    background-color: #f5f5f5;
    width: 12px;
}

QScrollBar::handle:vertical {
    background-color: #cccccc;
    border-radius: 6px;
}

QScrollBar::handle:vertical:hover {
    background-color: #999999;
}

QTabWidget::pane {
    border: 1px solid #cccccc;
}

QTabBar::tab {
    background-color: #e0e0e0;
    padding: 6px 20px;
    margin-right: 2px;
}

QTabBar::tab:selected {
    background-color: white;
}
"""
