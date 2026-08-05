"""
Repository para Guias - Padrão Repository
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from src.database.schema import Database
from src.models.guide import Guide, GuideHistory

class GuideRepository:
    """Repository para operações com guias"""
    
    def __init__(self, db: Database):
        self.db = db
    
    def get_all(self) -> List[Dict[str, Any]]:
        """Retorna todas as guias"""
        return self.db.get_all_guides()
    
    def get_by_id(self, guide_id: int) -> Optional[Dict[str, Any]]:
        """Retorna guia por ID"""
        return self.db.get_guide_by_id(guide_id)
    
    def get_by_numero(self, numero_guia: str) -> Optional[Dict[str, Any]]:
        """Retorna guia por número"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM guides WHERE numero_guia = ?', (numero_guia,))
        guide = cursor.fetchone()
        conn.close()
        return dict(guide) if guide else None
    
    def create(self, numero_guia: str, paciente: str, 
               status: str = "Guia emitida / liberada") -> bool:
        """Cria nova guia"""
        return self.db.add_guide(numero_guia, paciente, status)
    
    def update_status(self, guide_id: int, novo_status: str) -> bool:
        """Atualiza status e registra no histórico"""
        return self.db.update_guide_status(guide_id, novo_status)
    
    def mark_as_aware(self, guide_id: int) -> bool:
        """Marca guia como ciente"""
        return self.db.mark_as_aware(guide_id)
    
    def get_by_status(self, status: str) -> List[Dict[str, Any]]:
        """Retorna guias por status"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM guides WHERE status = ? ORDER BY ultima_alteracao DESC', (status,))
        guides = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return guides
    
    def get_pending_awareness(self) -> List[Dict[str, Any]]:
        """Retorna guias pendentes de ciência"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM guides WHERE ciencia_status = ? ORDER BY ultima_alteracao DESC',
            ("Pendente",)
        )
        guides = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return guides
    
    def get_updated_today(self) -> List[Dict[str, Any]]:
        """Retorna guias atualizadas hoje"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM guides 
            WHERE DATE(ultima_alteracao) = DATE('now')
            ORDER BY ultima_alteracao DESC
        ''')
        guides = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return guides
    
    def get_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Retorna guias em período específico"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM guides 
            WHERE DATE(ultima_alteracao) BETWEEN ? AND ?
            ORDER BY ultima_alteracao DESC
        ''', (start_date.date(), end_date.date()))
        guides = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return guides
    
    def filter_guides(self, status: Optional[str] = None,
                     pending_awareness: bool = False,
                     updated_today: bool = False,
                     start_date: Optional[datetime] = None,
                     end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """Filtra guias com múltiplos critérios"""
        guides = self.get_all()
        
        # Filtrar por status
        if status and status != "Todos":
            guides = [g for g in guides if g.get("status") == status]
        
        # Filtrar por ciência pendente
        if pending_awareness:
            guides = [g for g in guides if g.get("ciencia_status") == "Pendente"]
        
        # Filtrar por atualizadas hoje
        if updated_today:
            today = datetime.now().date()
            guides = [g for g in guides if (
                g.get("ultima_alteracao") and 
                (isinstance(g.get("ultima_alteracao"), str) and g.get("ultima_alteracao")[:10] == str(today) or
                 isinstance(g.get("ultima_alteracao"), datetime) and g.get("ultima_alteracao").date() == today)
            )]
        
        # Filtrar por período
        if start_date and end_date:
            guides = [g for g in guides if (
                g.get("ultima_alteracao") and
                (isinstance(g.get("ultima_alteracao"), str) and start_date.date() <= datetime.fromisoformat(g.get("ultima_alteracao")).date() <= end_date.date() or
                 isinstance(g.get("ultima_alteracao"), datetime) and start_date.date() <= g.get("ultima_alteracao").date() <= end_date.date())
            )]
        
        return guides
