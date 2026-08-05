from datetime import datetime, timedelta
from typing import List, Dict, Any
import random

class SimulatedSolusAdapter:
    """Adaptador simulado do Solus para testes"""
    
    # Lista de status possíveis (conforme imagem)
    STATUSES = [
        "Guia emitida / liberada",
        "Guia negada",
        "Guia cancelada",
        "Guia pedido/aguard confirmação",
        "Guia com setor de OPME",
        "Sob auditoria na Unimed origem",
        "Guia parcialmente liberada",
        "Cancelada na Unimed origem",
        "Negada na Unimed origem",
        "Guia sob auditoria"
    ]
    
    def __init__(self):
        self.guides = self._generate_simulated_data()
    
    def _generate_simulated_data(self) -> List[Dict[str, Any]]:
        """Gera dados simulados para demonstração"""
        pacientes = [
            "PEDRO HENRIQUE DA SILVA",
            "MARIA EDUARDA FERREIRA",
            "JOÃO VICTOR OLIVEIRA",
            "ANA CLARA BARROS",
            "CARLOS EDUARDO SOUZA",
            "LUIZ HENRIQUE GOMES",
            "ISABELLA MARTINS",
            "RENATO PEREIRA LIMA",
            "GABRIELA ALENCAR",
            "THIAGO FERNANDÊS"
        ]
        
        guides = []
        base_date = datetime.now()
        
        for i, paciente in enumerate(pacientes, 1):
            numero_guia = f"1162{4000 + i}"
            ultima_alter = base_date - timedelta(hours=random.randint(0, 48))
            ultima_consult = base_date - timedelta(hours=random.randint(0, 72))
            
            guides.append({
                "id": i,
                "numero_guia": numero_guia,
                "paciente": paciente,
                "status": random.choice(self.STATUSES),
                "ultima_consulta": ultima_consult,
                "ultima_alteracao": ultima_alter,
                "ciencia_status": random.choice(["Pendente", "Ciente"]),
                "ciencia_timestamp": ultima_alter if random.random() > 0.5 else None
            })
        
        return guides
    
    def get_guides(self) -> List[Dict[str, Any]]:
        """Retorna lista de guias simuladas"""
        return self.guides
    
    def get_guide_by_numero(self, numero_guia: str) -> Dict[str, Any]:
        """Retorna guia por número"""
        for guide in self.guides:
            if guide["numero_guia"] == numero_guia:
                return guide
        return None
    
    def update_guide_status(self, numero_guia: str, novo_status: str) -> bool:
        """Simula atualização de status"""
        for guide in self.guides:
            if guide["numero_guia"] == numero_guia:
                guide["status"] = novo_status
                guide["ultima_alteracao"] = datetime.now()
                return True
        return False
