
import socket

def download(req_file):
    print(req_file)

    ip = req_file["ip"]
    port = req_file["port"]

    peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        peer.connect((ip, port))
    except socket.error:
        peer.close()
        return 0, "Failed to connect to the Peer!"
    
    request_message = "DOWNLOAD: {}, {}, {}".format(req_file["name"], req_file["type"], req_file["size"])

    peer.send(request_message.encode())

    buffer = peer.recv(4096)

    if(buffer[:5] != "FILE: "):
        peer.close()
        return 0, "Peer is not responding correctly !"

    buffer = buffer[6:]

    while(len(buffer) < req_file["size"]):
        buffer += peer.recv(4096)
    
    # filename = req_file["dir"] + "/" + req_file["name"] + "." + req_file["type"]
    # out_file = open(filename, "wb")
    # out_file.write()


    


