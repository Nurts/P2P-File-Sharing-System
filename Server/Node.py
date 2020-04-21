

class Node:
    def __init__(self, fileType, fileSize, lastMod, ip, port, creator_ip, creator_port):
        self.fileType = fileType
        self.fileSize = fileSize
        self.lastMod = lastMod
        self.ip = ip
        self.port = port
        self.creator_ip = creator_ip
        self.creator_port = creator_port

    def __str__(self):
        return "<"+self.fileType+","+self.fileSize+","+self.lastMod+","+self.ip+","+self.port+">"

    def getCreator(self):
        return "(\'"+str(self.creator_ip)+"\',"+str(self.creator_port)+")"