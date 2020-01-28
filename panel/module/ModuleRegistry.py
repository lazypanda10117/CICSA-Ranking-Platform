from enum import Enum


class ModuleRegistry(Enum):
    MANAGEMENT_DATA = 0
    MANAGEMENT_EVENT = 1
    MANAGEMENT_RANKING = 2
    MANAGEMENT_NEWS = 3
    MANAGEMENT_LEAGUE = 4


class ModuleRegistryName:
    MANAGEMENT_DATA = 'data'
    MANAGEMENT_EVENT = 'event'
    MANAGEMENT_RANKING = 'ranking'
    MANAGEMENT_NEWS = 'news'
    MANAGEMENT_LEAGUE = 'league'

    def __getAppList__(self):
        return [
            self.MANAGEMENT_DATA,
            self.MANAGEMENT_EVENT,
            self.MANAGEMENT_RANKING,
            self.MANAGEMENT_NEWS,
            self.MANAGEMENT_LEAGUE
        ]