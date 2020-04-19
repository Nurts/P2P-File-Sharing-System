import tkinter as tk
from Listener import Listener
from Widgets import PlaceholderEntry
from Widgets import FocusButton
from Download import download_handler
import multiprocessing
import sys
# <pdf, 258, 07/30/2018, 192.168.0.5, 7777>

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
        self.listener = Listener("localhost", source_dir)
        print("Running On: {}".format(self.listener.get_self()))
        self.listen_thread = multiprocessing.Process(target=self.listener.listen)
        self.listen_thread.start()

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def search(self):
        text = self.search_bar.get()


        for i in range(10):
            self.listbox.insert(tk.END, text)

        

    def download(self):
        #<txt, 30, 07/30/2018, 127.0.0.1, 55038>
        data = self.listbox.get(tk.ACTIVE).strip()[1:-1].split(',')
        data = list(map(lambda str: str.strip(), data))
        status_message = "Nothing happened"
        status_color = "gray"

        if(len(data) != 5):
            status_message = "Failed to download data format is not correct!"
            status_color = "red"
        else:
            req_file = {
                "name" : "asd",#self.search_bar.get().strip()
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
        self.listen_thread.terminate()
        sys.exit()
        


if __name__ == "__main__":


    app = ClientApp("D:/Projects/P2P_File_Sharing/Downloads", "D:/Projects/P2P_File_Sharing/Files")
    app.mainloop()

    



