class BlockObject:
    def __init__(self, block_title, element_name, header, contents):
        self.block_title = block_title
        self.element_name = element_name
        self.header = header  # an array of headers corresponding to each element
        self.contents = contents  # a dictionary of elements

    def getBlockTitle(self):
        return self.block_title

    def getElementName(self):
        return self.element_name

    def getHeader(self):
        return self.header

    def getContents(self):
        return self.contents
