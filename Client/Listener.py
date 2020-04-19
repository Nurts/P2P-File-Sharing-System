import socket
import os
from threading import Thread

class Listener:
    def __init__(self, ip, dir_path):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((ip, 0))
        self.directory = dir_path
    
    def get_port(self):
        return self.socket.getsockname()[1]
    
    def listen(self):
        self.socket.listen(10)
        self.thread = None

        while True:
            peer_socket, peer_address = self.socket.accept()

            self.thread = Thread(target = self.peer_handler, args = (peer_socket, peer_address))

            self.thread.daemon = True
            self.thread.start()

    def peer_handler(self, peer_socket, peer_address):
        
        request = peer_socket.recv(4096).decode("utf-8")
        
        if(request[:8] != "DOWNLOAD:"):
            peer_socket.close()
            return
        
        data = request[9:-1].split(',')
        data = list(map(lambda str: str.strip(), data))
        file_data = {
            "path" : self.directory + "/" + data[0] + "." + data[1],
            "name" : data[0],
            "type" : data[1],
            "size" : data[2]
        }

        peer_socket.send("FILE: ")

        if os.path.isfile(file_data["path"]):

            sfile = open(file_data["path"], "rb")
            buffer = sfile.read(2048)
            while (len(buffer) > 0):
                peer_socket.send(buffer)
                buffer = sfile.read(2048)
        
        peer_socket.close()


            
        

        

        

        
                
            

        
