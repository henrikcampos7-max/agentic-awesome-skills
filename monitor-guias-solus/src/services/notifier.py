"""
Serviço de Notificações do Windows
"""

from typing import Optional
from datetime import datetime
import sys

try:
    from win10toast import ToastNotifier
    TOAST_AVAILABLE = True
except ImportError:
    TOAST_AVAILABLE = False

from src.utils.logger import LGPDLogger

class NotificationService:
    """Serviço para enviar notificações Windows"""
    
    def __init__(self, logger: LGPDLogger):
        self.logger = logger
        if TOAST_AVAILABLE and sys.platform == "win32":
            self.notifier = ToastNotifier()
        else:
            self.notifier = None
    
    def notify_status_change(self, numero_guia: str, paciente: str,
                             status_anterior: str, status_novo: str) -> bool:
        """Envia notificação de mudança de status"""
        titulo = f"Status de Guia Alterado"
        mensagem = f"""Guia: {numero_guia}
Paciente: {paciente}
Anterior: {status_anterior}
Atual: {status_novo}"""
        
        return self._send_notification(titulo, mensagem, numero_guia)
    
    def notify_pending_awareness(self, numero_guia: str, paciente: str) -> bool:
        """Envia notificação de guia pendente de ciência"""
        titulo = "Guia Pendente de Ciência"
        mensagem = f"""Guia: {numero_guia}
Paciente: {paciente}
Por favor, marque como ciente."""
        
        return self._send_notification(titulo, mensagem, numero_guia)
    
    def notify_sync_success(self, records_processed: int) -> bool:
        """Envia notificação de sincronização bem-sucedida"""
        titulo = "Sincronização Completa"
        mensagem = f"Registros processados: {records_processed}"
        
        return self._send_notification(titulo, mensagem)
    
    def notify_sync_error(self, error_message: str) -> bool:
        """Envia notificação de erro em sincronização"""
        titulo = "Erro na Sincronização"
        mensagem = f"Erro: {error_message}"
        
        return self._send_notification(titulo, mensagem)
    
    def _send_notification(self, titulo: str, mensagem: str,
                          numero_guia: Optional[str] = None) -> bool:
        """Envia notificação para o Windows"""
        try:
            if self.notifier:
                self.notifier.show_toast(
                    titulo,
                    mensagem,
                    duration=5,
                    threaded=True
                )
                
                # Registrar no log
                self.logger.log_notification_sent(numero_guia or "N/A", titulo)
                return True
            else:
                # Fallback para logging
                self.logger.logger.info(f"NOTIFICATION: {titulo} - {mensagem}")
                return True
        except Exception as e:
            self.logger.log_error(
                "NOTIFICATION_ERROR",
                str(e)
            )
            return False
