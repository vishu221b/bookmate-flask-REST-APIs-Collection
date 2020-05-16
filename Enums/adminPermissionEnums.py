from enum import Enum


class AdminPermissionEnums(Enum):
    GRANT = True
    REVOKE = False
    ACTIVATE = True
    DEACTIVATE = False
