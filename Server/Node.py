class Node:
    def __init__(self, fileType, fileSize, lastMod, ip, port):
        self.fileType = fileType
        self.fileSize = fileSize
        self.lastMod = lastMod
        self.ip = ip
        self.port = port

    def __str__(self):
        return "<"+self.fileType+","+self.fileSize+","+self.lastMod+","+self.ip+","+self.port+">"