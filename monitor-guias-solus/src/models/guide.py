from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class Guide:
    """Model para Guia"""
    numero_guia: str
    paciente: str
    status: str = "Guia emitida / liberada"
    ultima_consulta: Optional[datetime] = None
    ultima_alteracao: Optional[datetime] = None
    ciencia_status: str = "Pendente"
    ciencia_timestamp: Optional[datetime] = None
    id: Optional[int] = None
    
    def is_pending_awareness(self) -> bool:
        """Verifica se está pendente de ciência"""
        return self.ciencia_status == "Pendente"
    
    def is_updated_today(self) -> bool:
        """Verifica se foi atualizada hoje"""
        if not self.ultima_alteracao:
            return False
        return self.ultima_alteracao.date() == datetime.now().date()

@dataclass
class GuideHistory:
    """Model para Histórico de Guia"""
    guide_id: int
    status_anterior: Optional[str] = None
    status_novo: str = ""
    timestamp: Optional[datetime] = None
    usuario: str = "Sistema"
    observacoes: Optional[str] = None
    id: Optional[int] = None

@dataclass
class Settings:
    """Model para Configurações"""
    chave: str
    valor: str
    tipo: str = "string"
    id: Optional[int] = None
