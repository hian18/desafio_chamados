from enum import Enum


class UserRole(str, Enum):
    ADMIN = 'admin'
    TECHNICIAN = 'technician'
    AGENT = 'agent'


# Grupos de roles úteis
SUPPORT_UPDATE_ROLES = {UserRole.ADMIN, UserRole.TECHNICIAN}
SUPPORT_READ_ROLES = {UserRole.ADMIN, UserRole.TECHNICIAN}

AGENT_ROLES = {UserRole.AGENT}

