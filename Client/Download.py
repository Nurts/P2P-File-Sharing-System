#by Nurtas Ilyas and Askhat Kenenbay
import Helper
import socket

def download_handler(req_file):
    print(req_file)

    ip = req_file["ip"]
    port = req_file["port"]

    peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        peer.connect((ip, port))
    except socket.error as e:
        print(e)
        peer.close()
        return 0, "Failed to connect to the Peer!"
    
    request_message = "DOWNLOAD: {}, {}, {}".format(req_file["name"], req_file["type"], req_file["size"])
    
    try:
        peer.send(request_message.encode())
    except socket.error as e:
        peer.close()
        return 0, "Peer is not listening!"
    
    buffer = Helper.receive(peer, 4096)
    if(buffer is None):
        peer.close()
        return 0, "Peer is gone"

    # print(buffer[:6].decode("utf-8"))

    if(buffer[:6].decode("utf-8") != "FILE: "):
        peer.close()
        return 0, "Peer is not responding correctly !"

    buffer = buffer[6:]

    
    while(len(buffer) < req_file["size"]):
        new_data = Helper.receive(peer, 4096)
        if(new_data is None) or len(new_data) == 0:
            peer.close()
            return 0, "Peer is not sending the whole file!"
        
        buffer += new_data
        
    filename = req_file["dir"] + "/" + req_file["name"] + "." + req_file["type"]
    out_file = open(filename, "wb")
    out_file.write(buffer)
    out_file.close()

    peer.close()

    return 1, "File was downloaded successfully !"



    


