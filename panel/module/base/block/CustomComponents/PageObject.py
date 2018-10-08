class PageObject:
    def __init__(self, title, element_list, header, external=list()):
        self.title = title
        self.element_list = element_list
        self.header = header
        self.external = external

    def getTitle(self):
        return self.title

    def getElementList(self):
        return self.element_list

    def getHeader(self):
        return self.header

    def getExternal(self):
        return self.external
