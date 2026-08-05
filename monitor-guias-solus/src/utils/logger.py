"""
Logger com conformidade LGPD
"""

import logging
from datetime import datetime
from pathlib import Path
import json
from typing import Any, Dict, Optional

class LGPDLogger:
    """Logger com conformidade LGPD para auditoria"""
    
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Configurar logger
        self.logger = logging.getLogger("monitor_guias")
        self.logger.setLevel(logging.DEBUG)
        
        # Handler para arquivo
        handler = logging.FileHandler(
            self.log_dir / f"monitor_{datetime.now().strftime('%Y%m%d')}.log"
        )
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def log_guide_creation(self, numero_guia: str, paciente: str, usuario: str = "Sistema"):
        """Registra criação de guia"""
        self.logger.info(
            f"GUIDE_CREATED | numero_guia={numero_guia} | paciente={self._hash_pii(paciente)} | usuario={usuario}"
        )
    
    def log_guide_update(self, numero_guia: str, status_anterior: str, status_novo: str, usuario: str = "Sistema"):
        """Registra atualização de status"""
        self.logger.info(
            f"GUIDE_UPDATED | numero_guia={numero_guia} | status={status_anterior} -> {status_novo} | usuario={usuario}"
        )
    
    def log_awareness_marked(self, numero_guia: str, usuario: str = "Sistema"):
        """Registra marcação de ciência"""
        self.logger.info(
            f"AWARENESS_MARKED | numero_guia={numero_guia} | usuario={usuario}"
        )
    
    def log_sync_start(self):
        """Registra início de sincronização"""
        self.logger.info("SYNC_START | Iniciando sincronização com Solus")
    
    def log_sync_success(self, records_processed: int):
        """Registra sincronização bem-sucedida"""
        self.logger.info(f"SYNC_SUCCESS | records_processed={records_processed}")
    
    def log_sync_error(self, error_message: str):
        """Registra erro em sincronização"""
        self.logger.error(f"SYNC_ERROR | error={error_message}")
    
    def log_status_change_detected(self, numero_guia: str, status_anterior: str, status_novo: str):
        """Registra detecção de mudança de status"""
        self.logger.info(
            f"STATUS_CHANGE_DETECTED | numero_guia={numero_guia} | status={status_anterior} -> {status_novo}"
        )
    
    def log_notification_sent(self, numero_guia: str, titulo: str):
        """Registra notificação enviada"""
        self.logger.info(f"NOTIFICATION_SENT | numero_guia={numero_guia} | titulo={titulo}")
    
    def log_error(self, error_type: str, error_message: str, traceback: Optional[str] = None):
        """Registra erro técnico"""
        msg = f"ERROR | type={error_type} | message={error_message}"
        if traceback:
            msg += f" | traceback={traceback}"
        self.logger.error(msg)
    
    @staticmethod
    def _hash_pii(value: str) -> str:
        """Aplica hash a dados pessoais (PII) para conformidade LGPD"""
        # Em produção, usar bcrypt ou argon2
        import hashlib
        return f"hash({hashlib.md5(value.encode()).hexdigest()[:8]})"
