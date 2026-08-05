"""
Testes para Models
"""

import pytest
from datetime import datetime
from src.models.guide import Guide, GuideHistory, Settings

class TestGuideModel:
    """Testes para modelo Guide"""
    
    def test_create_guide(self):
        """Testa criação de guide"""
        guide = Guide(
            numero_guia="1162001",
            paciente="TESTE PACIENTE",
            status="Guia emitida / liberada"
        )
        
        assert guide.numero_guia == "1162001"
        assert guide.paciente == "TESTE PACIENTE"
        assert guide.status == "Guia emitida / liberada"
    
    def test_is_pending_awareness_true(self):
        """Testa se guia está pendente de ciência"""
        guide = Guide(
            numero_guia="1162001",
            paciente="TESTE PACIENTE",
            ciencia_status="Pendente"
        )
        
        assert guide.is_pending_awareness() is True
    
    def test_is_pending_awareness_false(self):
        """Testa se guia não está pendente de ciência"""
        guide = Guide(
            numero_guia="1162001",
            paciente="TESTE PACIENTE",
            ciencia_status="Ciente"
        )
        
        assert guide.is_pending_awareness() is False
    
    def test_is_updated_today_true(self):
        """Testa se guia foi atualizada hoje"""
        guide = Guide(
            numero_guia="1162001",
            paciente="TESTE PACIENTE",
            ultima_alteracao=datetime.now()
        )
        
        assert guide.is_updated_today() is True
    
    def test_is_updated_today_false(self):
        """Testa se guia não foi atualizada hoje"""
        from datetime import timedelta
        guide = Guide(
            numero_guia="1162001",
            paciente="TESTE PACIENTE",
            ultima_alteracao=datetime.now() - timedelta(days=5)
        )
        
        assert guide.is_updated_today() is False

class TestGuideHistoryModel:
    """Testes para modelo GuideHistory"""
    
    def test_create_history(self):
        """Testa criação de history"""
        history = GuideHistory(
            guide_id=1,
            status_anterior="Guia emitida / liberada",
            status_novo="Guia negada",
            usuario="teste_user"
        )
        
        assert history.guide_id == 1
        assert history.status_anterior == "Guia emitida / liberada"
        assert history.status_novo == "Guia negada"
        assert history.usuario == "teste_user"

class TestSettingsModel:
    """Testes para modelo Settings"""
    
    def test_create_settings(self):
        """Testa criação de settings"""
        settings = Settings(
            chave="sync_interval",
            valor="60",
            tipo="integer"
        )
        
        assert settings.chave == "sync_interval"
        assert settings.valor == "60"
        assert settings.tipo == "integer"
