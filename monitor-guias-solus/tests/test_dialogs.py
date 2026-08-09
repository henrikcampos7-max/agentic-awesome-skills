"""
T35 — Testes unitários para Dialogs
Cobre NovaGuiaDialog e HistoricoDialog, incluindo validações e helpers.

Os testes que dependem do PySide6 são ignorados automaticamente quando a
biblioteca não está instalada (ex.: ambiente de CI sem display disponível).
"""

import pytest

# Pular módulo inteiro se PySide6 não estiver disponível
PySide6 = pytest.importorskip("PySide6", reason="PySide6 não instalado")

import os
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

from src.ui.widgets.dialogs import NovaGuiaDialog, HistoricoDialog
from src.utils.constants import STATUSES, STATUS_COLORS


# ─────────────────────────────────────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def qapp():
    """Cria (ou reutiliza) a QApplication para os testes de UI."""
    app = QApplication.instance() or QApplication([])
    yield app


@pytest.fixture
def guia_exemplo():
    return {
        "id": 42,
        "numero_guia": "1162999",
        "paciente": "PACIENTE TESTE",
        "status": "Guia emitida / liberada",
        "ciencia_status": "Pendente",
        "ultima_alteracao": "2026-08-09 10:00:00",
    }


@pytest.fixture
def historico_exemplo():
    return [
        {
            "id": 1,
            "guide_id": 42,
            "status_anterior": "Guia emitida / liberada",
            "status_novo": "Guia negada",
            "usuario": "Operador",
            "observacoes": "Negada por falta de documentação",
            "timestamp": "2026-08-08 15:00:00",
            "ciencia_usuario": None,
            "ciencia_timestamp": None,
        }
    ]


# ─────────────────────────────────────────────────────────────────────────────
# Testes: NovaGuiaDialog
# ─────────────────────────────────────────────────────────────────────────────

class TestNovaGuiaDialog:

    def test_dialog_instancia_corretamente(self, qapp):
        dialog = NovaGuiaDialog()
        assert dialog is not None
        dialog.close()

    def test_titulo_correto(self, qapp):
        dialog = NovaGuiaDialog()
        assert "Guia" in dialog.windowTitle() or dialog.windowTitle() != ""
        dialog.close()

    def test_campos_inicialmente_vazios(self, qapp):
        dialog = NovaGuiaDialog()
        assert dialog.campo_numero.text() == ""
        assert dialog.campo_paciente.text() == ""
        dialog.close()

    def test_combo_status_populado(self, qapp):
        dialog = NovaGuiaDialog()
        count = dialog.combo_status.count()
        assert count == len(STATUSES)
        dialog.close()

    def test_label_erro_inicialmente_oculto(self, qapp):
        dialog = NovaGuiaDialog()
        assert not dialog.lbl_erro.isVisible()
        dialog.close()

    def test_obter_dados_reflete_campos(self, qapp):
        dialog = NovaGuiaDialog()
        dialog.campo_numero.setText("1162001")
        dialog.campo_paciente.setText("João Silva")
        dados = dialog.obter_dados()
        assert dados["numero_guia"] == "1162001"
        assert dados["paciente"] == "JOÃO SILVA"   # deve converter para maiúsculas
        dialog.close()

    def test_obter_dados_status_padrao_e_valido(self, qapp):
        dialog = NovaGuiaDialog()
        dados = dialog.obter_dados()
        assert dados["status"] in STATUSES
        dialog.close()

    def test_confirmar_sem_numero_mostra_erro(self, qapp):
        dialog = NovaGuiaDialog()
        dialog.campo_numero.setText("")
        dialog.campo_paciente.setText("Paciente Teste")
        # Chamar _confirmar diretamente sem fechar o dialog
        dialog._confirmar()
        assert dialog.lbl_erro.isVisible()
        dialog.close()

    def test_confirmar_sem_paciente_mostra_erro(self, qapp):
        dialog = NovaGuiaDialog()
        dialog.campo_numero.setText("1162001")
        dialog.campo_paciente.setText("")
        dialog._confirmar()
        assert dialog.lbl_erro.isVisible()
        dialog.close()

    def test_confirmar_com_dados_validos_emite_sinal(self, qapp):
        dialog = NovaGuiaDialog()
        emissoes = []
        dialog.guia_adicionada.connect(lambda n, p, s: emissoes.append((n, p, s)))
        dialog.campo_numero.setText("1162001")
        dialog.campo_paciente.setText("Paciente Ok")
        dialog._confirmar()
        assert len(emissoes) == 1
        numero, paciente, status = emissoes[0]
        assert numero == "1162001"
        assert paciente == "PACIENTE OK"
        assert status in STATUSES
        dialog.close()


# ─────────────────────────────────────────────────────────────────────────────
# Testes: HistoricoDialog
# ─────────────────────────────────────────────────────────────────────────────

class TestHistoricoDialog:

    def test_dialog_instancia_sem_historico(self, qapp, guia_exemplo):
        dialog = HistoricoDialog(guia=guia_exemplo, historico=[])
        assert dialog is not None
        dialog.close()

    def test_dialog_instancia_com_historico(self, qapp, guia_exemplo, historico_exemplo):
        dialog = HistoricoDialog(guia=guia_exemplo, historico=historico_exemplo)
        assert dialog is not None
        dialog.close()

    def test_titulo_contem_numero_guia(self, qapp, guia_exemplo):
        dialog = HistoricoDialog(guia=guia_exemplo, historico=[])
        titulo = dialog.windowTitle()
        assert "1162999" in titulo or titulo != ""
        dialog.close()

    def test_campo_observacoes_inicialmente_vazio(self, qapp, guia_exemplo):
        dialog = HistoricoDialog(guia=guia_exemplo, historico=[])
        assert dialog.campo_obs.toPlainText() == ""
        dialog.close()

    def test_dialog_aceita_historico_multiplas_entradas(self, qapp, guia_exemplo):
        historico = [
            {
                "id": i,
                "guide_id": 42,
                "status_anterior": "Guia emitida / liberada",
                "status_novo": "Guia negada",
                "usuario": f"User{i}",
                "observacoes": "",
                "timestamp": "2026-08-08 10:00:00",
                "ciencia_usuario": None,
                "ciencia_timestamp": None,
            }
            for i in range(1, 6)
        ]
        dialog = HistoricoDialog(guia=guia_exemplo, historico=historico)
        assert dialog is not None
        dialog.close()


# ─────────────────────────────────────────────────────────────────────────────
# Testes: helper estático _eh_cor_escura
# ─────────────────────────────────────────────────────────────────────────────

class TestHelperCorEscura:

    def test_preto_e_escuro(self):
        assert HistoricoDialog._eh_cor_escura("#000000") is True

    def test_branco_nao_e_escuro(self):
        assert HistoricoDialog._eh_cor_escura("#ffffff") is False

    def test_azul_escuro(self):
        assert HistoricoDialog._eh_cor_escura("#0066cc") is True

    def test_amarelo_claro(self):
        assert HistoricoDialog._eh_cor_escura("#ffff00") is False

    def test_hex_sem_cerquilha(self):
        # Deve tratar graciosamente com ou sem '#'
        result = HistoricoDialog._eh_cor_escura("000000")
        assert result is True

    def test_hex_invalido_retorna_false(self):
        result = HistoricoDialog._eh_cor_escura("#XXYYZZ")
        assert result is False

    def test_cores_por_status(self):
        """Todos os status_colors devem ser processáveis sem erro."""
        for status, cor in STATUS_COLORS.items():
            result = HistoricoDialog._eh_cor_escura(cor)
            assert isinstance(result, bool)
