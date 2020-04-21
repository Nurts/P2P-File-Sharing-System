#by Nurtas Ilyas and Askhat Kenenbay
import tkinter as tk
import tkinter.messagebox
from Listener import Listener
from Widgets import PlaceholderEntry
from Widgets import FocusButton
from Download import download_handler
from Sender import Sender
import multiprocessing
import sys
import json
import os.path

# Configure this values
host = "localhost"
downloads_folder = "../Downloads"
share_folder = "../Files"
#Server Ip and port should be here
ft_server = "127.0.0.1" , 2558



class ClientApp(tk.Tk):
    def __init__(self, download_dir, source_dir):
        self.download_dir = download_dir
        tk.Tk.__init__(self)
        self.title("Torrent Sucks")
        self.geometry("500x500+300+100")
        self.resizable(False, True)
        self.config(bg = "#474040")
        
        self.frame = tk.Frame(self, bg = '#474040')
        self.frame.pack(side = tk.TOP, fill = tk.BOTH)
        
        self.search_bar = PlaceholderEntry(self.frame, "Please Enter the Filename", width = 50)
        self.search_bar.pack(side = tk.LEFT, pady = 20, padx = 20)
        
        self.search_button = FocusButton(self.frame, text = "Search", in_color = "gray", out_color = "black", fg = "white", command =  self.search)
        self.search_button.pack(side = tk.RIGHT, padx = 20, pady = 20)


        self.listbox_frame = tk.Frame(self, bg = "#474040")
        self.listbox_frame.pack(side = tk.TOP, fill = tk.BOTH)

        self.listbox = tk.Listbox(self.listbox_frame, width = 70, height = 20)
        self.listbox.pack(side = tk.TOP, pady = 20, padx = 20)


        self.download_button = FocusButton(self.listbox_frame, text = "Download", in_color = "#52bf9c", out_color = "#6ed1ff", fg = "black", command = self.download)
        self.download_button.pack(side = tk.RIGHT, pady = 20, padx = 20)

        self.status_text = tk.Label(self.listbox_frame, text = "", bg = "#474040", font='Helvetica 10 bold')
        self.status_text.pack(side = tk.LEFT, pady = 20, padx = 20)

        #Start listener
        global host
        self.listener = Listener(host, source_dir)
        self.host, self.port = self.listener.get_self()

        print("Running On: {}:{}".format(self.host, self.port))

        self.listen_thread = multiprocessing.Process(target=self.listener.listen)
        self.listen_thread.start()

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.search_file = ""

        #Start Sender
        
        self.sender = Sender(source_dir, self.host, self.port)
        
        
        global ft_server
#Uncomment this if server is on
        print("Connecting to Server...")
        # print(ft_server[0])
        # print(ft_server[1])
        status = self.sender.start_conn(ft_server[0], ft_server[1])
        if(status == 0):
            tkinter.messagebox.showerror(title="Error", message="Couldn't correctly connect to FT server!\nCheck the ip configuration in Client.py, and restart the app!")


# If server is not ready this will say "Could not connect to server"
    def search(self):
        filename = self.search_bar.get().strip()
        self.search_file = filename
        self.listbox.delete(0, tk.END)
        succ, status_message = self.sender.search(filename)

        if not succ:
            self.status_text.configure(text = status_message, fg = "red")
            

        else:
            self.status_text.configure(text = "")
            for result in self.sender.get_results():
                self.listbox.insert(tk.END, result.strip())

        

    def download(self):
        #<jpg, 54280, 07/30/2018, 127.0.0.1, 55682>
        data = self.listbox.get(tk.ACTIVE).strip()[1:-1].split(',')
        data = list(map(lambda str: str.strip(), data))
        status_message = "Nothing happened"
        status_color = "gray"

        if(len(data) != 5):
            status_message = "Failed to download data format is not correct!"
            status_color = "red"
        else:
            req_file = {
                "name" : self.search_file,#self.search_bar.get().strip()
                "type" : data[0],
                "size" : int(data[1]),
                "date" : data[2],
                "ip" : data[3],
                "port" : int(data[4]),
                "dir" : self.download_dir
            }
            succ, status_message = download_handler(req_file)
            if(succ):
                status_color = "green"
            else:
                status_color = "red"

        
        self.status_text.configure(text = status_message, fg = status_color)
    
    def on_closing(self):
        print("Closing!")
        self.sender.close()

        self.listen_thread.terminate()
        sys.exit()
        


if __name__ == "__main__":
    if not os.path.exists(downloads_folder):
        print("Download dir is not correct")
        tkinter.messagebox.showerror(title="Error", message="Download directory do not exist !\n Please check Client.py 'download_folder'")
        sys.exit(-1)
    if not os.path.exists(share_folder):
        print("Sharing Folder is not correct")
        tkinter.messagebox.showerror(title="Error", message="Sharing directory do not exist !\n Please check Client.py 'share_folder'")
        sys.exit(-1)

    app = ClientApp(downloads_folder, share_folder)
    app.mainloop()

    



