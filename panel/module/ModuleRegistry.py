from enum import Enum


class ModuleRegistry(Enum):
    # Core Apps are not exposed to public.
    CORE_DATA = -1
    MANAGEMENT_DATA = 0
    MANAGEMENT_EVENT = 1
    MANAGEMENT_RANKING = 2
    MANAGEMENT_NEWS = 3
    MANAGEMENT_LEAGUE = 4
