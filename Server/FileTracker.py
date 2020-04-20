import os
import signal
import socket
import sys
from Node import Node
from threading import Thread

configuration_file = ""
configuration = {}
# hashMap<fileName, List<Node> >
hashMap = {}
clients = {}
    
def method(connection, address, incoming):
    print("address"+str(address[0])+":"+str(address[1]))
    print("message received: "+str(incoming))
    message = str(incoming)
    message = message[2:len(message)-1]
    if message == "HELLO":
        print("message==HELLO")
        connection.send(b"HI")
        fileList = connection.recv(8132).decode("utf-8").strip()
        if fileList is None:
            print("Greedy client")
            return 0
        count = 0
        print(fileList)
        fileList = fileList.replace("<","")
        fileList = fileList.replace(">","")
        myList = fileList.split('|')

        for myFile in myList:
            print(myFile)
            temp = myFile.split(',')
            if len(temp) == 6:
                node = Node(temp[1],temp[2],temp[3],temp[4],temp[5])
                hashMap[temp[0]] = node
                count = count + 1
            if count == 5:
                break
        if count != 0:
            clients[address[0]] = address[1]
        print("Files send: ")
        print(count)
        print(hashMap)
        # we are not closing connection, need false
        return 1==0
    elif message == "BYE":
        print("message==BYE")
        connection.close()
        # remove from clients
        print("Closing connection with"+str(address))
        del clients[address[0]]
        # remove from hashMap?????
        # we are closing connection, need true
        return 1==1
    search = message[0:6]
    if search == "SEARCH":
        print("message==SEARCHs")
        # we are not closing connection, need false
        return 1==0


def client_function(connection, address):
    """
    connection : connection socket
    address : (IP_address, port)
    """
    while True:
        incoming = connection.recv(4096)
        close_connection = method(connection, address, incoming)
        if close_connection:
            break

def main():
    global clients
    global hashMap

    # create an INET, STREAMing socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind the socket to a public host, and a well-known port
    server_socket.bind(('127.0.0.1', 2558))
    # become a server socket
    server_socket.listen(5)

    # handle incoming client connections
    client_counter = 0
    print("/0")
    while True:
        connection, address = server_socket.accept()
        # cli_output
        # output message
        print("a client connected from {}:{}".format(address[0], str(address[1])))

        # create a thread that runs the client_function
        client_thread = Thread(name="client {}".format(client_counter),
                target=client_function, args=(connection, address))

        # TODO
        # handle differently, terminate gracefully
        client_thread.daemon = True
        client_thread.start()

        client_counter += 1

if __name__ == "__main__":
    main()
