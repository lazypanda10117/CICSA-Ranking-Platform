class PageObject:
    def __init__(
        self, 
        title, 
        element_list=None, 
        header=None, 
        external=None, 
        element=None, 
        context=None
    ):
        self.title = title
        self.element = element
        self.element_list = element_list
        self.header = header
        self.external = external
        self.context = context

    def getTitle(self):
        return self.title

    def getElementList(self):
        return self.element_list

    def getHeader(self):
        return self.header

    def getExternal(self):
        return self.external

    def getContext(self):
        return self.context

    def getElement(self):
        return self.element