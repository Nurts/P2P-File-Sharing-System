import os
import signal
import socket
import sys
from Node import Node
from threading import Thread

# hashMap<fileName, List<Node> >
hashMap = {}
clients = {}
    
def method(connection, address, incoming):
    print("address: "+str(address))
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
                node = Node(temp[1],temp[2],temp[3],temp[4],temp[5], address[0],address[1])
                nodeList = hashMap.get(temp[0])
                if nodeList is None:
                    nodeList = []
                nodeList.append(node)
                hashMap[temp[0]] = nodeList
                count = count + 1
            if count == 5:
                break
        if count != 0:
            clients[address[0]] = address[1]
        print("Files send: ")
        print(count)
        print(clients)
        print(hashMap)
        # we are not closing connection, need false
        return 1==0

    # validate client
    if address[0] in clients :
        print("")
    else:
        return 1==0
    
    if message == "BYE":
        print("message==BYE")
        connection.close()
        # remove from clients
        print("Closing connection with"+str(address))
        print("before BYE:")
        print(hashMap)
        print(clients)
        print("--------------------------")
        del clients[address[0]]
        # remove from hashMap
        removeKey = []
        for key in hashMap:
            nodeList = hashMap.get(key)
            for node in nodeList:
                if node.creator_ip == address[0] and  node.creator_port == address[1]:
                    nodeList.remove(node)
                    if len(nodeList) ==0:
                        removeKey.append(key)
        for key in removeKey:
            del hashMap[key]
        print("after BYE:")
        print(hashMap)
        print(clients)
        print("--------------------------")
        # we are closing connection, need true
        return 1==1
    search = message[0:6]
    if search == "SEARCH":
        print("message==SEARCH")
        search = message[8:]
        print("Searching for: "+search)
        if search in hashMap:
            output = "FOUND: "
            nodeList = hashMap.get(search)
            for node in nodeList:
                output = output + str(node)
            # byte_output = bytes(output, 'utf-8')
            # connection.send(byte_output)
            print(output)
            connection.send(output.encode('utf-8'))
        else:
            print("NOT FOUND")
            connection.send(b"NOT FOUND")
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
