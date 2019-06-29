class Dispatcher:
    def __init__(self):
        self.dispatchTable = dict()

    def exists(self, link_name):
        return link_name in self.dispatchTable


    def add(self, link_name, link_obj):
        self.dispatchTable[link_name] = link_obj

    def get(self, link_name):
        if link_name not in self.dispatchTable:
            raise Exception("Cannot get {} from Dispatcher".format(link_name))
        return self.dispatchTable[link_name]

    def update(self, link_name, link_obj):
        self.dispatchTable[link_name] = link_obj

    def delete(self, link_name):
        if link_name not in self.dispatchTable:
            raise Exception("Cannot delete {} from Dispatcher".format(link_name))
        del self.dispatchTable[link_name]
