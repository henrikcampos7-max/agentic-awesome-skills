"""
Testes para GuideRepository
"""

import pytest
from datetime import datetime, timedelta
from src.database.schema import Database
from src.services.repository import GuideRepository
import os

@pytest.fixture
def test_repo():
    """Fixture para repository de teste"""
    db_path = "test_repository.db"
    db = Database(db_path=db_path)
    repo = GuideRepository(db)
    yield repo
    # Cleanup
    if os.path.exists(db_path):
        os.remove(db_path)

class TestGuideRepository:
    """Testes para GuideRepository"""
    
    def test_create_guide(self, test_repo):
        """Testa criação de guia"""
        result = test_repo.create("1162001", "TESTE PACIENTE", "Guia emitida / liberada")
        assert result is True
    
    def test_get_all_guides(self, test_repo):
        """Testa retorno de todas as guias"""
        test_repo.create("1162001", "PACIENTE 1", "Guia emitida / liberada")
        test_repo.create("1162002", "PACIENTE 2", "Guia negada")
        
        guides = test_repo.get_all()
        assert len(guides) == 2
    
    def test_get_by_id(self, test_repo):
        """Testa busca por ID"""
        test_repo.create("1162001", "TESTE PACIENTE")
        guide = test_repo.get_by_id(1)
        
        assert guide is not None
        assert guide["numero_guia"] == "1162001"
    
    def test_get_by_numero(self, test_repo):
        """Testa busca por número"""
        test_repo.create("1162001", "TESTE PACIENTE")
        guide = test_repo.get_by_numero("1162001")
        
        assert guide is not None
        assert guide["paciente"] == "TESTE PACIENTE"
    
    def test_get_by_status(self, test_repo):
        """Testa filtro por status"""
        test_repo.create("1162001", "PACIENTE 1", "Guia emitida / liberada")
        test_repo.create("1162002", "PACIENTE 2", "Guia negada")
        test_repo.create("1162003", "PACIENTE 3", "Guia emitida / liberada")
        
        guides = test_repo.get_by_status("Guia emitida / liberada")
        assert len(guides) == 2
    
    def test_get_pending_awareness(self, test_repo):
        """Testa filtro de guias pendentes de ciência"""
        test_repo.create("1162001", "PACIENTE 1")
        test_repo.create("1162002", "PACIENTE 2")
        test_repo.mark_as_aware(1)
        
        pending = test_repo.get_pending_awareness()
        assert len(pending) == 1
        assert pending[0]["numero_guia"] == "1162002"
    
    def test_update_status(self, test_repo):
        """Testa atualização de status"""
        test_repo.create("1162001", "TESTE PACIENTE", "Guia emitida / liberada")
        result = test_repo.update_status(1, "Guia negada")
        
        assert result is True
        guide = test_repo.get_by_id(1)
        assert guide["status"] == "Guia negada"
    
    def test_mark_as_aware(self, test_repo):
        """Testa marcação de ciência"""
        test_repo.create("1162001", "TESTE PACIENTE")
        result = test_repo.mark_as_aware(1)
        
        assert result is True
        guide = test_repo.get_by_id(1)
        assert guide["ciencia_status"] == "Ciente"
    
    def test_filter_guides_by_status(self, test_repo):
        """Testa filtro combinado por status"""
        test_repo.create("1162001", "PACIENTE 1", "Guia emitida / liberada")
        test_repo.create("1162002", "PACIENTE 2", "Guia negada")
        
        guides = test_repo.filter_guides(status="Guia emitida / liberada")
        assert len(guides) == 1
        assert guides[0]["numero_guia"] == "1162001"
    
    def test_filter_guides_all_status(self, test_repo):
        """Testa que 'Todos' retorna todas as guias"""
        test_repo.create("1162001", "PACIENTE 1", "Guia emitida / liberada")
        test_repo.create("1162002", "PACIENTE 2", "Guia negada")
        
        guides = test_repo.filter_guides(status="Todos")
        assert len(guides) == 2
    
    def test_filter_guides_by_pending_awareness(self, test_repo):
        """Testa filtro de guias pendentes de ciência"""
        test_repo.create("1162001", "PACIENTE 1")
        test_repo.create("1162002", "PACIENTE 2")
        test_repo.mark_as_aware(1)
        
        guides = test_repo.filter_guides(pending_awareness=True)
        assert len(guides) == 1
