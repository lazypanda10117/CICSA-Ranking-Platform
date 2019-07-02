from abc import ABC, abstractmethod


class ArchiveModel(ABC):
    def __init__(self):
        self.some_properties = "hi"

    @abstractmethod
    def somefunction(self):
        pass