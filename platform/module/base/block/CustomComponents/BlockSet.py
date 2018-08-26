class BlockSet():
    def __init__(self):
        self.blocks = []

    def getBlocks(self):
        return self.blocks;

    def addBlock(self, block):
        self.blocks.append(block);

    def makeBlockSet(self, *args):
        for block in args:
            self.addBlock(block);
        return self;
