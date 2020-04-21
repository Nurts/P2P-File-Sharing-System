#by Nurtas Ilyas and Askhat Kenenbay
import socket
import os
import time
import Helper

class Sender:
    def __init__(self, share_folder, ip, port):
        #You can change separator from here ->
        self.separator = '|'

        files = []

        for r, _, f in os.walk(share_folder):
            for file_ in f:
                data = {
                    "name" : file_,
                    "path" : os.path.join(r, file_),
                    "ip" : ip,
                    "port" : port
                }

                files.append(data)

        for data in files:
            data["size"]  = os.path.getsize(data["path"])
            data["name"], data["type"] = os.path.splitext(data["name"])
            data["type"] = data["type"][1:]
            data["date"] = time.strftime('%d/%m/%Y', time.localtime( os.path.getmtime(data["path"]) ))

        self.file_info = []

        for data in files:
            self.file_info.append( "<{}, {}, {}, {}, {}, {}>".format(
                data["name"], data["type"], data["size"], data["date"], data["ip"], data["port"])  )
        
        self.server = None
        self.results = []

    def start_conn(self, ip, port):
        
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.server.connect((ip, port))
        except socket.error as e:
            self.server.close()
            self.server = None
            print("FT Server is not responding ! Error: {}".format(e))
            return 0
        
        try:
            self.server.send(b"HELLO")
        except socket.error as e:
            print("FT Server is not listening ! Error: {}".format(e))
            return 0


        data_in = Helper.receive(self.server, 4096)
        if(data_in is None):
            print("FT Server is not responding ! Error: {}".format(e))
            return 0
        
        response = data_in.decode("utf-8").strip()

        if(response != "HI"):
            print("FT Server is not responding correctly !")
            return 0
        
        num = 0
        message = ""
        

        for file_ in self.file_info:

            if(len(message) > 0):
                message += self.separator
            
            message += file_
            num += 1
            if(num == 5):
                break

        try:
            self.server.send(message.encode())
        except socket.error as e:
            print("FT Server is not listening! Error: {}".format(e))
            return 0        
        
        return 1

    def search(self, filename):
        
        if(self.server is None):
            print("You are not connected to server !")
            return 0, "Couldn't connect to server!"

        message = "SEARCH: {}".format(filename)
        
        try:
            self.server.send(message.encode())
        except socket.error as e:
            print("Server is not listening! Error: {}".format(e))
            return 0, "Server is not listening!"


        buffer = Helper.receive(self.server, 8192)
        if(buffer is None):
            return 0, "Server is not responding! Maybe you're greedy!"

        buffer = buffer.decode("utf-8")
        
        
        if(buffer == "NOT FOUND"):
            return 0, "{} was not found on server!".format(filename)
        
        if(buffer[:6] != "FOUND:"):
            return 0, "Server responded in wrong format !"
        
        #Don't know what kind of separator should be between records I chose '|'
        
        self.results = buffer[6:].split(self.separator)

        return 1, ""
    
    def get_results(self):
        return self.results

        
    def close(self):
        if self.server == None:
            return
        try:
            self.server.send(b"BYE")
        except socket.error as e:
            print("Server is not listening! Error {}".format(e))
        print('BYE!')
        self.server.close()


if __name__ == "__main__":
    sender = Sender("../Files", "127.0.0.1", 2558)