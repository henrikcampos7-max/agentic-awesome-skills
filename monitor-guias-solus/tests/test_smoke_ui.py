"""
T37 — Smoke test de inicialização da UI
Verifica que os componentes principais instanciam sem crash.

Pula automaticamente quando PySide6 não está disponível.
"""

import pytest
import os

PySide6 = pytest.importorskip("PySide6", reason="PySide6 não instalado")

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication
from src.database.schema import Database


# ─────────────────────────────────────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance() or QApplication([])
    yield app


@pytest.fixture
def db_temporario(tmp_path):
    return Database(db_path=str(tmp_path / "smoke_test.db"))


# ─────────────────────────────────────────────────────────────────────────────
# Smoke: componentes de UI instanciam sem exceção
# ─────────────────────────────────────────────────────────────────────────────

class TestSmokeUI:

    def test_database_abre_sem_crash(self, db_temporario):
        """Banco de dados inicializa sem erros."""
        assert db_temporario is not None

    def test_main_window_instancia(self, qapp, db_temporario):
        """MainWindow instancia sem lançar exceção."""
        from src.ui.main_window import MainWindow
        # Substituímos o db padrão pelo de teste via patch manual
        import unittest.mock as mock
        with mock.patch("src.ui.main_window.Database", return_value=db_temporario):
            win = MainWindow(usuario="smoke_user")
        assert win is not None
        win.close()

    def test_main_window_titulo(self, qapp, db_temporario):
        """Janela principal tem título definido."""
        from src.ui.main_window import MainWindow
        import unittest.mock as mock
        with mock.patch("src.ui.main_window.Database", return_value=db_temporario):
            win = MainWindow()
        assert win.windowTitle() != ""
        win.close()

    def test_main_window_usuario_propagado(self, qapp, db_temporario):
        """Usuário logado é propagado para a janela principal."""
        from src.ui.main_window import MainWindow
        import unittest.mock as mock
        with mock.patch("src.ui.main_window.Database", return_value=db_temporario):
            win = MainWindow(usuario="usuario_smoke")
        assert win.usuario_logado == "usuario_smoke"
        win.close()

    def test_login_dialog_instancia(self, qapp, db_temporario):
        """LoginDialog instancia sem lançar exceção."""
        from src.ui.login import LoginDialog
        import unittest.mock as mock
        with mock.patch("src.ui.login.Database", return_value=db_temporario):
            dlg = LoginDialog()
        assert dlg is not None
        dlg.close()

    def test_configuracoes_dialog_instancia(self, qapp, db_temporario):
        """ConfiguracoesDialog instancia sem lançar exceção."""
        from src.ui.configuracoes import ConfiguracoesDialog
        import unittest.mock as mock
        with mock.patch("src.ui.configuracoes.Database", return_value=db_temporario):
            dlg = ConfiguracoesDialog()
        assert dlg is not None
        dlg.close()

    def test_nova_guia_dialog_instancia(self, qapp):
        """NovaGuiaDialog instancia sem lançar exceção."""
        from src.ui.widgets.dialogs import NovaGuiaDialog
        dlg = NovaGuiaDialog()
        assert dlg is not None
        dlg.close()

    def test_historico_dialog_instancia(self, qapp):
        """HistoricoDialog instancia sem lançar exceção."""
        from src.ui.widgets.dialogs import HistoricoDialog
        guia = {
            "id": 1,
            "numero_guia": "1162001",
            "paciente": "SMOKE PACIENTE",
            "status": "Guia emitida / liberada",
            "ciencia_status": "Pendente",
            "ultima_alteracao": "2026-08-09 10:00:00",
        }
        dlg = HistoricoDialog(guia=guia, historico=[])
        assert dlg is not None
        dlg.close()

    def test_dashboard_panel_instancia(self, qapp):
        """DashboardPanel instancia sem lançar exceção."""
        from src.ui.widgets.dashboard import DashboardPanel
        panel = DashboardPanel()
        assert panel is not None

    def test_guides_table_instancia(self, qapp):
        """GuidesTable instancia sem lançar exceção."""
        from src.ui.widgets.table import GuidesTable
        table = GuidesTable()
        assert table is not None

    def test_filters_panel_instancia(self, qapp):
        """FiltersPanel instancia sem lançar exceção."""
        from src.ui.widgets.filters import FiltersPanel
        panel = FiltersPanel()
        assert panel is not None
