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

# Cores para status — design system "Clinical Precision" (design/stitch/DESIGN.md)
STATUS_COLORS = {
    "Guia emitida / liberada": "#15803D",  # Status verde (Autorizada/aprovada)
    "Guia negada": "#BA1A1A",  # Status vermelho (Negada)
    "Guia cancelada": "#E5484D",  # Vermelho claro (Cancelada)
    "Guia pedido/aguard confirmação": "#B45309",  # Status âmbar (Pendente)
    "Guia com setor de OPME": "#7C3AED",  # Púrpura (Em fluxo interno)
    "Sob auditoria na Unimed origem": "#2563EB",  # Status azul (Em análise)
    "Guia parcialmente liberada": "#EA580C",  # Status laranja (Expirada/alerta)
    "Cancelada na Unimed origem": "#6B7280",  # Cinza médio (Fechada)
    "Negada na Unimed origem": "#9CA3AF",  # Cinza claro (Fechada)
    "Guia sob auditoria": "#006065"  # Teal primário (Sob auditoria)
}

# Sincronização
SYNC_INTERVAL_MINUTES = 60  # A cada 60 minutos
