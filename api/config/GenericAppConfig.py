import json
from abc import ABC
from abc import abstractmethod


class GenericAppConfig(ABC):
    def __init__(self):
        self.base_path = 'api/config/'
        self.specific_config_path = self.getConfigFilesPath()
        self.config_dispatcher = self.setConfigDispatcher()

    @abstractmethod
    def getConfigFilesPath(self):
        pass

    @abstractmethod
    def setConfigDispatcher(self):
        pass

    def __getAbsolutePathToConfigFiles(self, identifier):
        return self.base_path + self.specific_config_path + self.config_dispatcher.get(identifier)

    def getData(self, identifier):
        with open(self.__getAbsolutePathToConfigFiles(identifier)) as config_json:
            config = json.load(config_json)
            return config
