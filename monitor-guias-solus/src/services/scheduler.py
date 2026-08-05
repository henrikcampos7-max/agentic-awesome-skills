"""
Scheduler para sincronização automática
"""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from typing import Callable, Optional
from src.utils.logger import LGPDLogger

class SyncScheduler:
    """Agendador para sincronização periódica"""
    
    def __init__(self, logger: LGPDLogger, interval_minutes: int = 60):
        self.logger = logger
        self.interval_minutes = interval_minutes
        self.scheduler = BackgroundScheduler()
        self.sync_callback: Optional[Callable] = None
    
    def set_sync_callback(self, callback: Callable):
        """Define callback para sincronização"""
        self.sync_callback = callback
    
    def start(self):
        """Inicia o agendador"""
        try:
            # Adicionar job de sincronização
            self.scheduler.add_job(
                self._sync_task,
                trigger=IntervalTrigger(minutes=self.interval_minutes),
                id='sync_guides',
                name='Sincronizar Guias',
                replace_existing=True
            )
            
            if not self.scheduler.running:
                self.scheduler.start()
                self.logger.logger.info(f"SCHEDULER_STARTED | interval={self.interval_minutes} minutos")
        except Exception as e:
            self.logger.log_error("SCHEDULER_START_ERROR", str(e))
    
    def stop(self):
        """Para o agendador"""
        try:
            if self.scheduler.running:
                self.scheduler.shutdown()
                self.logger.logger.info("SCHEDULER_STOPPED")
        except Exception as e:
            self.logger.log_error("SCHEDULER_STOP_ERROR", str(e))
    
    def _sync_task(self):
        """Tarefa de sincronização"""
        try:
            self.logger.log_sync_start()
            
            if self.sync_callback:
                result = self.sync_callback()
                if result:
                    self.logger.log_sync_success(result.get('records_processed', 0))
                else:
                    self.logger.log_sync_error("Callback retornou erro")
        except Exception as e:
            self.logger.log_sync_error(str(e))
    
    def trigger_manual_sync(self):
        """Força sincronização manual"""
        try:
            self._sync_task()
            return True
        except Exception as e:
            self.logger.log_error("MANUAL_SYNC_ERROR", str(e))
            return False
