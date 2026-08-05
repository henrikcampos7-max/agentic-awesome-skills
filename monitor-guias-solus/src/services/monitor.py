"""
Serviço de Monitor para comparar status e detectar mudanças
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
from src.services.repository import GuideRepository
from src.utils.logger import LGPDLogger

class MonitorService:
    """Serviço para monitorar e detectar mudanças de status"""
    
    def __init__(self, repository: GuideRepository, logger: LGPDLogger):
        self.repository = repository
        self.logger = logger
        self.previous_states: Dict[int, str] = {}  # Armazena estado anterior
    
    def check_status_changes(self) -> List[Dict[str, Any]]:
        """
        Compara status anterior com atual e retorna mudanças detectadas
        """
        changes = []
        guides = self.repository.get_all()
        
        for guide in guides:
            guide_id = guide.get("id")
            current_status = guide.get("status")
            previous_status = self.previous_states.get(guide_id)
            
            # Se há mudança de status
            if previous_status and previous_status != current_status:
                change = {
                    "guide_id": guide_id,
                    "numero_guia": guide.get("numero_guia"),
                    "paciente": guide.get("paciente"),
                    "status_anterior": previous_status,
                    "status_novo": current_status,
                    "timestamp": datetime.now()
                }
                changes.append(change)
                
                # Registrar no log
                self.logger.log_status_change_detected(
                    guide.get("numero_guia"),
                    previous_status,
                    current_status
                )
            
            # Atualizar estado anterior
            self.previous_states[guide_id] = current_status
        
        return changes
    
    def get_monitoring_summary(self) -> Dict[str, Any]:
        """Retorna resumo de monitoramento"""
        guides = self.repository.get_all()
        
        summary = {
            "total_guides": len(guides),
            "em_monitoramento": len(guides),
            "atualizadas_hoje": len(self.repository.get_updated_today()),
            "pendentes_ciencia": len(self.repository.get_pending_awareness()),
            "erros": 0  # Implementar detecção de erros
        }
        
        return summary
    
    def get_status_distribution(self) -> Dict[str, int]:
        """Retorna distribuição de status"""
        guides = self.repository.get_all()
        distribution = {}
        
        for guide in guides:
            status = guide.get("status", "Desconhecido")
            distribution[status] = distribution.get(status, 0) + 1
        
        return distribution
    
    def maintain_last_valid_status(self, guide_id: int, fallback_status: str) -> bool:
        """
        Em caso de erro técnico, mantém último status válido
        """
        guide = self.repository.get_by_id(guide_id)
        if guide and guide.get("status"):
            return True
        
        # Se erro, restaurar status anterior
        if guide_id in self.previous_states:
            self.repository.update_status(guide_id, self.previous_states[guide_id])
            self.logger.log_error(
                "STATUS_RESTORE",
                f"Restaurando status anterior para guia {guide_id}"
            )
            return True
        
        # Se não há status anterior, usar fallback
        self.repository.update_status(guide_id, fallback_status)
        return True
