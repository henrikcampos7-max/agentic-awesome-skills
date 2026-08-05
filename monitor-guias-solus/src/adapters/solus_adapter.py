from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class SolusAdapterInterface(ABC):
    """Interface para adaptadores Solus"""
    
    @abstractmethod
    def get_guides(self) -> List[Dict[str, Any]]:
        """Retorna lista de guias"""
        pass
    
    @abstractmethod
    def get_guide_by_numero(self, numero_guia: str) -> Optional[Dict[str, Any]]:
        """Retorna guia por número"""
        pass
    
    @abstractmethod
    def update_guide_status(self, numero_guia: str, novo_status: str) -> bool:
        """Atualiza status de uma guia"""
        pass
