"""
Constantes compartilhadas entre apps para evitar dependências circulares.
"""

# Choices para ações de histórico
ACTION_CHOICES = [
    ('created', 'Created'),
    ('edited', 'Edited'),
    ('removed', 'Removed'),
    ('other', 'Other'),
]

# Choices para status de cavaletes
CAVALETE_STATUS_CHOICES = [
    ('available', 'Available'),
    ('assigned', 'Assigned'),
    ('inactive', 'Inactive'),
]

# Choices para tipos de cavaletes
CAVALETE_TYPE_CHOICES = [
    ('corredor', 'Corredor'),
    ('torre', 'Torre'),
]

# Choices para lados de slots
SLOT_SIDE_CHOICES = [
    ('A', 'Side A'),
    ('B', 'Side B'),
]

# Choices para status de slots
SLOT_STATUS_CHOICES = [
    ('available', 'Available'),
    ('auditing', 'Auditing'),
    ('awaiting_approval', 'Awaiting Approval'),
    ('completed', 'Completed'),
]

# Choices para roles de usuário
ROLE_CHOICES = [
    ('admin', 'Administrador'),
    ('manager', 'Gestor'),
    ('auditor', 'Conferente'),
]
