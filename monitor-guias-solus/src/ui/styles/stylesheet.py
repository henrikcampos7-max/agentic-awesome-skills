"""
Stylesheet principal da aplicação.

Implementa o design system "Clinical Precision" (export do Google Stitch em
`design/stitch/`): paleta teal/verde Unimed, fundo cool-gray, cartões brancos
com borda sutil, cantos suaves e tipografia Inter (com fallbacks).
"""

# Tokens do design system (fonte: design/stitch/DESIGN.md)
COLORS = {
    "background": "#f7fafa",          # surface / background
    "surface": "#ffffff",             # cards e containers
    "surface_dim": "#ebeeee",
    "zebra": "#f1f4f4",               # linhas alternadas de tabela
    "border": "#e2e8f0",              # bordas (outline-variant)
    "outline": "#bdc9c9",
    "on_surface": "#181c1d",          # texto principal
    "on_surface_variant": "#3e4949",  # texto secundário
    "primary": "#006065",             # teal (verde Unimed derivado)
    "primary_hover": "#00767c",
    "primary_pressed": "#004f53",
    "primary_container": "#0d7a80",
    "on_primary": "#ffffff",
    "error": "#ba1a1a",
    "focus": "#00696e",
}

STYLESHEET = f"""
QMainWindow {{
    background-color: {COLORS["background"]};
}}

QWidget {{
    background-color: {COLORS["background"]};
    color: {COLORS["on_surface"]};
    font-family: "Inter", "Segoe UI", "Arial", sans-serif;
    font-size: 13px;
}}

QLabel {{
    color: {COLORS["on_surface"]};
}}

QPushButton {{
    background-color: {COLORS["primary"]};
    color: {COLORS["on_primary"]};
    border: none;
    border-radius: 4px;
    padding: 8px 16px;
    font-weight: 600;
    font-size: 12px;
}}

QPushButton:hover {{
    background-color: {COLORS["primary_hover"]};
}}

QPushButton:pressed {{
    background-color: {COLORS["primary_pressed"]};
}}

QPushButton:disabled {{
    background-color: {COLORS["outline"]};
    color: #ffffff;
}}

QLineEdit, QComboBox {{
    border: 1px solid {COLORS["border"]};
    border-radius: 4px;
    padding: 8px;
    background-color: {COLORS["surface"]};
    color: {COLORS["on_surface"]};
}}

QLineEdit:hover, QComboBox:hover {{
    border-color: {COLORS["outline"]};
}}

QLineEdit:focus, QComboBox:focus {{
    border: 2px solid {COLORS["focus"]};
}}

QComboBox::drop-down {{
    border: none;
    width: 22px;
}}

QTableWidget {{
    background-color: {COLORS["surface"]};
    alternate-background-color: {COLORS["zebra"]};
    gridline-color: {COLORS["border"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 8px;
    selection-background-color: {COLORS["primary_container"]};
    selection-color: #ffffff;
}}

QTableWidget::item {{
    padding: 8px 6px;
    border: none;
    background: transparent;
}}

QTableWidget::item:selected {{
    background-color: {COLORS["primary_container"]};
    color: #ffffff;
}}

QTableWidget::item:alternate {{
    background-color: {COLORS["zebra"]};
}}

QHeaderView::section {{
    background-color: {COLORS["surface_dim"]};
    color: {COLORS["on_surface_variant"]};
    padding: 8px 6px;
    border: none;
    border-bottom: 1px solid {COLORS["outline"]};
    font-weight: 600;
}}

QGroupBox {{
    border: 1px solid {COLORS["border"]};
    border-radius: 8px;
    margin-top: 10px;
    padding: 12px 8px 8px 8px;
    background-color: {COLORS["surface"]};
    color: {COLORS["on_surface"]};
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 3px 0 3px;
    color: {COLORS["on_surface_variant"]};
}}

QCheckBox {{
    spacing: 6px;
    color: {COLORS["on_surface"]};
}}

QCheckBox::indicator {{
    width: 18px;
    height: 18px;
    border: 1px solid {COLORS["outline"]};
    border-radius: 4px;
    background-color: {COLORS["surface"]};
}}

QCheckBox::indicator:checked {{
    background-color: {COLORS["primary"]};
    border-color: {COLORS["primary"]};
}}

QFrame#separador {{
    background-color: {COLORS["border"]};
    max-height: 1px;
}}

QScrollBar:vertical {{
    background-color: {COLORS["background"]};
    width: 12px;
}}

QScrollBar::handle:vertical {{
    background-color: {COLORS["outline"]};
    border-radius: 6px;
    min-height: 24px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: #94a1a1;
}}

QScrollBar:horizontal {{
    background-color: {COLORS["background"]};
    height: 12px;
}}

QScrollBar::handle:horizontal {{
    background-color: {COLORS["outline"]};
    border-radius: 6px;
    min-width: 24px;
}}

QScrollBar::add-line, QScrollBar::sub-line {{
    height: 0px;
    width: 0px;
}}

QTabWidget::pane {{
    border: 1px solid {COLORS["border"]};
    border-radius: 8px;
}}

QTabBar::tab {{
    background-color: {COLORS["surface_dim"]};
    color: {COLORS["on_surface_variant"]};
    padding: 6px 20px;
    margin-right: 2px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    font-weight: 600;
}}

QTabBar::tab:selected {{
    background-color: {COLORS["surface"]};
    color: {COLORS["primary"]};
    border-bottom: 2px solid {COLORS["primary"]};
}}

QTabBar::tab:hover {{
    color: {COLORS["primary"]};
}}

QMessageBox {{
    background-color: {COLORS["background"]};
}}
"""