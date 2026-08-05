"""
Testes para Services
"""

import pytest
from src.database.schema import Database
from src.services.repository import GuideRepository
from src.services.monitor import MonitorService
from src.services.history import HistoryService
from src.utils.logger import LGPDLogger
import os

@pytest.fixture
def test_services():
    """Fixture para services de teste"""
    db_path = "test_services.db"
    db = Database(db_path=db_path)
    repo = GuideRepository(db)
    logger = LGPDLogger(log_dir="test_logs")
    
    services = {
        "db": db,
        "repo": repo,
        "logger": logger,
        "monitor": MonitorService(repo, logger),
        "history": HistoryService(db, logger)
    }
    yield services
    # Cleanup
    if os.path.exists(db_path):
        os.remove(db_path)

class TestMonitorService:
    """Testes para MonitorService"""
    
    def test_get_monitoring_summary(self, test_services):
        """Testa resumo de monitoramento"""
        repo = test_services["repo"]
        monitor = test_services["monitor"]
        
        repo.create("1162001", "PACIENTE 1")
        repo.create("1162002", "PACIENTE 2")
        
        summary = monitor.get_monitoring_summary()
        assert summary["total_guides"] == 2
        assert summary["em_monitoramento"] == 2
    
    def test_status_distribution(self, test_services):
        """Testa distribuição de status"""
        repo = test_services["repo"]
        monitor = test_services["monitor"]
        
        repo.create("1162001", "PACIENTE 1", "Guia emitida / liberada")
        repo.create("1162002", "PACIENTE 2", "Guia emitida / liberada")
        repo.create("1162003", "PACIENTE 3", "Guia negada")
        
        dist = monitor.get_status_distribution()
        assert dist["Guia emitida / liberada"] == 2
        assert dist["Guia negada"] == 1
    
    def test_check_status_changes(self, test_services):
        """Testa detecção de mudanças de status"""
        repo = test_services["repo"]
        monitor = test_services["monitor"]
        
        repo.create("1162001", "PACIENTE 1", "Guia emitida / liberada")
        monitor.check_status_changes()  # Registra estado inicial
        
        repo.update_status(1, "Guia negada")
        changes = monitor.check_status_changes()
        
        assert len(changes) == 1
        assert changes[0]["status_anterior"] == "Guia emitida / liberada"
        assert changes[0]["status_novo"] == "Guia negada"

class TestHistoryService:
    """Testes para HistoryService"""
    
    def test_get_guide_history(self, test_services):
        """Testa obtenção de histórico"""
        repo = test_services["repo"]
        history = test_services["history"]
        
        repo.create("1162001", "PACIENTE 1")
        repo.update_status(1, "Guia negada")
        repo.update_status(1, "Guia cancelada")
        
        hist = history.get_guide_history(1)
        assert len(hist) == 2
    
    def test_add_history_entry(self, test_services):
        """Testa adição de entrada ao histórico"""
        repo = test_services["repo"]
        history = test_services["history"]
        
        repo.create("1162001", "PACIENTE 1")
        result = history.add_history_entry(
            1,
            "Guia emitida / liberada",
            "Guia negada",
            usuario="teste_user"
        )
        
        assert result is True
        hist = history.get_guide_history(1)
        assert len(hist) == 1
