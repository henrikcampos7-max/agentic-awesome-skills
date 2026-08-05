"""
Constantes da aplicação
"""

# Status possíveis
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

# Cores para status
STATUS_COLORS = {
    "Guia emitida / liberada": "#FFFFFF",  # Branco
    "Guia negada": "#FF0000",  # Vermelho
    "Guia cancelada": "#FF6B6B",  # Vermelho claro
    "Guia pedido/aguard confirmação": "#FFD700",  # Amarelo
    "Guia com setor de OPME": "#9932CC",  # Púrpura
    "Sob auditoria na Unimed origem": "#87CEEB",  # Azul claro
    "Guia parcialmente liberada": "#FFA500",  # Laranja
    "Cancelada na Unimed origem": "#00CED1",  # Turquesa
    "Negada na Unimed origem": "#D3D3D3",  # Cinza
    "Guia sob auditoria": "#228B22"  # Verde escuro
}

# Sincronização
SYNC_INTERVAL_MINUTES = 60  # A cada 60 minutos
