"""
T34 — Testes de integração end-to-end
Exercita o fluxo completo: Database → GuideRepository → MonitorService → HistoryService
"""

import os
import pytest
from src.database.schema import Database
from src.services.repository import GuideRepository
from src.services.monitor import MonitorService
from src.services.history import HistoryService
from src.utils.logger import LGPDLogger


# ─────────────────────────────────────────────────────────────────────────────
# Fixture compartilhada
# ─────────────────────────────────────────────────────────────────────────────

@pytest.fixture
def stack(tmp_path):
    """Fixture que cria a pilha completa de serviços com banco isolado."""
    db_path = str(tmp_path / "test_integration.db")
    db = Database(db_path=db_path)
    logger = LGPDLogger(log_dir=str(tmp_path / "logs"))
    repo = GuideRepository(db)
    monitor = MonitorService(repo, logger)
    history = HistoryService(db, logger)
    return {"db": db, "repo": repo, "monitor": monitor, "history": history}


# ─────────────────────────────────────────────────────────────────────────────
# Fluxo: criar guia e consultar pelo repository
# ─────────────────────────────────────────────────────────────────────────────

class TestIntegrationCriarConsultar:

    def test_criar_guia_e_recuperar_por_numero(self, stack):
        repo = stack["repo"]
        repo.create("9900001", "PACIENTE INTEGRAÇÃO", "Guia emitida / liberada")
        guia = repo.get_by_numero("9900001")
        assert guia is not None
        assert guia["paciente"] == "PACIENTE INTEGRAÇÃO"
        assert guia["status"] == "Guia emitida / liberada"

    def test_criar_multiplas_guias_e_listar(self, stack):
        repo = stack["repo"]
        repo.create("9900010", "PACIENTE A", "Guia emitida / liberada")
        repo.create("9900011", "PACIENTE B", "Guia negada")
        repo.create("9900012", "PACIENTE C", "Guia cancelada")
        todas = repo.get_all()
        assert len(todas) == 3

    def test_get_by_status_filtra_corretamente(self, stack):
        repo = stack["repo"]
        repo.create("9900020", "PACIENTE X", "Guia emitida / liberada")
        repo.create("9900021", "PACIENTE Y", "Guia negada")
        emitidas = repo.get_by_status("Guia emitida / liberada")
        negadas = repo.get_by_status("Guia negada")
        assert len(emitidas) == 1
        assert len(negadas) == 1

    def test_nao_permite_numero_guia_duplicado(self, stack):
        repo = stack["repo"]
        ok1 = repo.create("9900030", "PRIMEIRO", "Guia emitida / liberada")
        ok2 = repo.create("9900030", "SEGUNDO", "Guia negada")
        assert ok1 is True
        assert ok2 is False
        todas = repo.get_all()
        assert len(todas) == 1


# ─────────────────────────────────────────────────────────────────────────────
# Fluxo: atualizar status e verificar histórico
# ─────────────────────────────────────────────────────────────────────────────

class TestIntegrationAtualizarStatus:

    def test_atualizar_status_persiste_no_banco(self, stack):
        repo = stack["repo"]
        repo.create("9900040", "PACIENTE STATUS", "Guia emitida / liberada")
        guia = repo.get_by_numero("9900040")
        ok = repo.update_status(guia["id"], "Guia negada")
        assert ok is True
        guia_atualizada = repo.get_by_id(guia["id"])
        assert guia_atualizada["status"] == "Guia negada"

    def test_historico_registrado_apos_mudanca_status(self, stack):
        repo = stack["repo"]
        db = stack["db"]
        repo.create("9900050", "PACIENTE HIST", "Guia emitida / liberada")
        guia = repo.get_by_numero("9900050")
        repo.update_status(guia["id"], "Sob auditoria na Unimed origem")
        historico = db.get_history(guia["id"])
        assert len(historico) >= 1
        ultimo = historico[0]
        assert ultimo["status_novo"] == "Sob auditoria na Unimed origem"


# ─────────────────────────────────────────────────────────────────────────────
# Fluxo: MonitorService detecta mudanças de status
# ─────────────────────────────────────────────────────────────────────────────

class TestIntegrationMonitorService:

    def test_sem_guias_sem_mudancas(self, stack):
        monitor = stack["monitor"]
        changes = monitor.check_status_changes()
        assert changes == []

    def test_resumo_com_guias(self, stack):
        repo = stack["repo"]
        monitor = stack["monitor"]
        repo.create("9900060", "PACIENTE MON", "Guia emitida / liberada")
        resumo = monitor.get_monitoring_summary()
        assert resumo["total_guides"] == 1
        assert resumo["em_monitoramento"] == 1

    def test_detecta_mudanca_de_status(self, stack):
        repo = stack["repo"]
        monitor = stack["monitor"]
        repo.create("9900070", "PACIENTE DETECT", "Guia emitida / liberada")
        # Primeira chamada inicializa o estado anterior
        monitor.check_status_changes()
        # Mudar status no banco
        guia = repo.get_by_numero("9900070")
        repo.update_status(guia["id"], "Guia negada")
        # Segunda chamada detecta a mudança
        changes = monitor.check_status_changes()
        assert len(changes) == 1
        assert changes[0]["status_anterior"] == "Guia emitida / liberada"
        assert changes[0]["status_novo"] == "Guia negada"

    def test_distribuicao_de_status(self, stack):
        repo = stack["repo"]
        monitor = stack["monitor"]
        repo.create("9900080", "P1", "Guia emitida / liberada")
        repo.create("9900081", "P2", "Guia emitida / liberada")
        repo.create("9900082", "P3", "Guia negada")
        dist = monitor.get_status_distribution()
        assert dist.get("Guia emitida / liberada") == 2
        assert dist.get("Guia negada") == 1

    def test_fallback_mantem_status_valido(self, stack):
        repo = stack["repo"]
        monitor = stack["monitor"]
        repo.create("9900090", "PACIENTE FALLBACK", "Guia emitida / liberada")
        guia = repo.get_by_numero("9900090")
        monitor.check_status_changes()  # Inicializar estado
        ok = monitor.maintain_last_valid_status(guia["id"], "Guia cancelada")
        assert ok is True


# ─────────────────────────────────────────────────────────────────────────────
# Fluxo: HistoryService adiciona e recupera entradas
# ─────────────────────────────────────────────────────────────────────────────

class TestIntegrationHistoryService:

    def test_adicionar_e_recuperar_historico(self, stack):
        repo = stack["repo"]
        history = stack["history"]
        repo.create("9900100", "PACIENTE HIS", "Guia emitida / liberada")
        guia = repo.get_by_numero("9900100")
        ok = history.add_history_entry(
            guia["id"],
            "Guia emitida / liberada",
            "Guia negada",
            usuario="TestUser",
            observacoes="Teste integração"
        )
        assert ok is True
        entradas = history.get_guide_history(guia["id"])
        assert len(entradas) >= 1
        assert entradas[0]["status_novo"] == "Guia negada"
        assert entradas[0]["usuario"] == "TestUser"

    def test_historico_vazio_para_guia_sem_alteracoes(self, stack):
        repo = stack["repo"]
        history = stack["history"]
        repo.create("9900110", "PACIENTE LIMPO", "Guia emitida / liberada")
        guia = repo.get_by_numero("9900110")
        entradas = history.get_guide_history(guia["id"])
        assert entradas == []


# ─────────────────────────────────────────────────────────────────────────────
# Fluxo: Ciência integrada
# ─────────────────────────────────────────────────────────────────────────────

class TestIntegrationCiencia:

    def test_marcar_ciencia_remove_da_lista_pendentes(self, stack):
        repo = stack["repo"]
        repo.create("9900120", "PACIENTE CIENCIA", "Guia negada")
        guia = repo.get_by_numero("9900120")
        # Deve aparecer como pendente (nova guia tem ciência Pendente por padrão)
        pendentes_antes = repo.get_pending_awareness()
        assert any(g["id"] == guia["id"] for g in pendentes_antes)
        # Marcar como ciente
        ok = repo.mark_as_aware(guia["id"])
        assert ok is True
        pendentes_depois = repo.get_pending_awareness()
        assert not any(g["id"] == guia["id"] for g in pendentes_depois)

    def test_filtro_pendentes_ciencia(self, stack):
        repo = stack["repo"]
        repo.create("9900130", "PENDENTE 1", "Guia negada")
        repo.create("9900131", "PENDENTE 2", "Guia cancelada")
        guia1 = repo.get_by_numero("9900130")
        repo.mark_as_aware(guia1["id"])
        pendentes = repo.get_pending_awareness()
        numeros = [g["numero_guia"] for g in pendentes]
        assert "9900130" not in numeros
        assert "9900131" in numeros


# ─────────────────────────────────────────────────────────────────────────────
# Fluxo: filtros avançados do Repository
# ─────────────────────────────────────────────────────────────────────────────

class TestIntegrationFiltros:

    def test_filtrar_por_status(self, stack):
        repo = stack["repo"]
        repo.create("9900140", "FILTRO A", "Guia emitida / liberada")
        repo.create("9900141", "FILTRO B", "Guia negada")
        resultado = repo.filter_guides(status="Guia negada")
        assert all(g["status"] == "Guia negada" for g in resultado)
        assert len(resultado) == 1

    def test_filtrar_pendentes_ciencia(self, stack):
        repo = stack["repo"]
        repo.create("9900150", "FILTRO CIENC A", "Guia emitida / liberada")
        repo.create("9900151", "FILTRO CIENC B", "Guia negada")
        guia_a = repo.get_by_numero("9900150")
        repo.mark_as_aware(guia_a["id"])
        resultado = repo.filter_guides(pending_awareness=True)
        numeros = [g["numero_guia"] for g in resultado]
        assert "9900150" not in numeros
        assert "9900151" in numeros
