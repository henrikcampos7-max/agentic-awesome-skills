"""
Testes para Database
"""

import pytest
import sqlite3
import os
from src.database.schema import Database

@pytest.fixture
def test_db():
    """Fixture para banco de dados de teste"""
    db_path = "test_monitor_guias.db"
    db = Database(db_path=db_path)
    yield db
    # Cleanup
    if os.path.exists(db_path):
        os.remove(db_path)

class TestDatabase:
    """Testes para a classe Database"""
    
    def test_init_creates_database(self, test_db):
        """Testa se o banco é criado corretamente"""
        assert os.path.exists("test_monitor_guias.db")
    
    def test_add_guide_success(self, test_db):
        """Testa adição bem-sucedida de guia"""
        result = test_db.add_guide("1162001", "TESTE PACIENTE", "Guia emitida / liberada")
        assert result is True
    
    def test_add_guide_duplicate_fails(self, test_db):
        """Testa que não permite duplicatas"""
        test_db.add_guide("1162001", "TESTE PACIENTE", "Guia emitida / liberada")
        result = test_db.add_guide("1162001", "OUTRO PACIENTE", "Guia negada")
        assert result is False
    
    def test_get_all_guides_empty(self, test_db):
        """Testa retorno vazio quando não há guias"""
        guides = test_db.get_all_guides()
        assert guides == []
    
    def test_get_all_guides_with_data(self, test_db):
        """Testa retorno de todas as guias"""
        test_db.add_guide("1162001", "PACIENTE 1", "Guia emitida / liberada")
        test_db.add_guide("1162002", "PACIENTE 2", "Guia negada")
        
        guides = test_db.get_all_guides()
        assert len(guides) == 2
        assert guides[0]["numero_guia"] == "1162002"  # Ordenado por data DESC
    
    def test_get_guide_by_id(self, test_db):
        """Testa busca de guia por ID"""
        test_db.add_guide("1162001", "TESTE PACIENTE", "Guia emitida / liberada")
        guide = test_db.get_guide_by_id(1)
        
        assert guide is not None
        assert guide["numero_guia"] == "1162001"
        assert guide["paciente"] == "TESTE PACIENTE"
    
    def test_get_guide_by_id_not_found(self, test_db):
        """Testa busca de guia inexistente"""
        guide = test_db.get_guide_by_id(999)
        assert guide is None
    
    def test_update_guide_status(self, test_db):
        """Testa atualização de status"""
        test_db.add_guide("1162001", "TESTE PACIENTE", "Guia emitida / liberada")
        result = test_db.update_guide_status(1, "Guia negada")
        
        assert result is True
        guide = test_db.get_guide_by_id(1)
        assert guide["status"] == "Guia negada"
    
    def test_mark_as_aware(self, test_db):
        """Testa marcação de ciência"""
        test_db.add_guide("1162001", "TESTE PACIENTE", "Guia emitida / liberada")
        result = test_db.mark_as_aware(1)
        
        assert result is True
        guide = test_db.get_guide_by_id(1)
        assert guide["ciencia_status"] == "Ciente"
    
    def test_get_history(self, test_db):
        """Testa histórico de guia"""
        test_db.add_guide("1162001", "TESTE PACIENTE", "Guia emitida / liberada")
        test_db.update_guide_status(1, "Guia negada")
        test_db.update_guide_status(1, "Guia cancelada")
        
        history = test_db.get_history(1)
        assert len(history) == 2
        assert history[0]["status_novo"] == "Guia cancelada"
        assert history[1]["status_novo"] == "Guia negada"
