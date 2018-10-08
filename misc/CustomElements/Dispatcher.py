class Dispatcher:
    def __init__(self):
        self.dispatchTable = {}

    def add(self, link_name, link_obj):
        self.dispatchTable[link_name] = link_obj

    def get(self, link_name):
        return self.dispatchTable[link_name]

    def update(self, link_name, link_obj):
        self.dispatchTable[link_name] = link_obj

    def delete(self, link_name):
        del self.dispatchTable[link_name]