import socket
import select

def receive(socket, buffsize):
    ready = select.select([socket], [], [], 2)
    data = None
    if(ready[0]):
        data = socket.recv(buffsize)
    
    return data