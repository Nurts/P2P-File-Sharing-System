#by Nurtas Ilyas and Askhat Kenenbay
import socket
import select

def receive(my_socket, buffsize):
    ready = select.select([my_socket], [], [], 2)
    data = None
    if(ready[0]):
        try:
            data = my_socket.recv(buffsize)
        except socket.error as e:
            print("Error: {}".format(e))
            return None
    
    return data