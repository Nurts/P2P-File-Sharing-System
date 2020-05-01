# P2P-File-Sharing-System
P2P File sharing Application by Nurtas Ilyas and Askhat Kenenbay

Clients could search for file (only type filename without extension).

Then Select the peer and press Download button to download file to your Download folder (specified in Client.py)

By default dowload directory and sharing directory are Download and Files folders, respectively

Instructions:

Go to directory Server and run Server.py
```python
> python Server.py
```
Go to directory Client and run Client.py
```python
> python Client.py
```
You can configure following values in Client.py
ft_server should be ip and port of FTServer
```python
host = "localhost"
downloads_folder = "../Downloads"
share_folder = "../Files"
ft_server = "127.0.0.1" , 2558
```

You can configure the following values in Server.py.
Port should be available
```python
server_port = 2558
server_ip = '127.0.0.1'
```

