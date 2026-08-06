"""
Entry point da aplicação Monitor de Guias Solus.
Fluxo: inicializa banco → exibe tela de Login → abre MainWindow com usuário autenticado.
"""

import sys
from PySide6.QtWidgets import QApplication
from src.database.schema import Database
from src.ui.login import LoginDialog
from src.ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Monitor de Guias Solus")
    app.setApplicationVersion("1.1.0")

    # Banco compartilhado entre Login e MainWindow
    db = Database()

    # T27/T28: exibir tela de Login
    login = LoginDialog(db)
    usuario_logado = None

    def ao_autenticar(usuario: str):
        nonlocal usuario_logado
        usuario_logado = usuario

    login.login_realizado.connect(ao_autenticar)

    if login.exec() != LoginDialog.Accepted or not usuario_logado:
        sys.exit(0)  # Usuário fechou o login sem autenticar

    # Abrir janela principal com o usuário autenticado
    window = MainWindow(usuario=usuario_logado)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
