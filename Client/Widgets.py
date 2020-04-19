import tkinter as tk

class FocusButton(tk.Button):
    def on_enter(self, event):
        self.configure(bg = self.in_color)
    
    def on_leave(self, event):
        self.configure(bg = self.out_color)

    def __init__(self, parent, in_color, out_color, **kwargs):
        self.in_color = in_color
        self.out_color = out_color
        tk.Button.__init__(self, parent, bg = out_color, **kwargs)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        


class Radiobuttons(tk.Frame):

    def __init__(self, parent, **kwargs):
        tk.Frame.__init__(self, parent, kwargs)
        self.value = tk.IntVar()
    
    def add(self, labels = []):
        for i in range(len(labels)):
            widget = tk.Radiobutton(self, text = labels[i], variable = self.value, value = i)
            widget.pack(side = tk.LEFT)

    def clear(self):
        self.value.set(0)


class RawFrame(tk.Frame):

    def __init__(self, parent, **kwargs):
        tk.Frame.__init__(self, parent, kwargs)
        self.widgets = []
    
    def add(self, labels = [], entry_width = []):
        
        for i in range(len(labels)):
            widget = None
            if(labels[i] == "Blank"):
                widget = tk.Label(self, text = "", width = entry_width[i])
            else:
                widget = LabelEntry(self, labels[i], entry_width[i])
                
            widget.pack(side = tk.LEFT, fill = tk.X, expand = True)
            self.widgets.append(widget)
    
    def change_info(self, info = []):
        for i in range(len(info)):
            self.widgets[i].change_entry(text = info[i])

    def getByIdx(self, idx):
        if(idx < len(self.widgets) and idx >= 0):
            return self.widgets[idx].get()
        else:
            return None

    def clear(self):
        for widget in self.widgets:
            if(isinstance(widget, LabelEntry)):
                widget.clear()

class LabelEntry(tk.Frame):

    def __init__(self, parent, text, entry_width = 10, **kwargs):
        tk.Frame.__init__(self, parent, kwargs)
        self.label = tk.Label(self, text = text, font = 'Helvetica 10', bg  = self["background"], anchor = 'w')
        self.label.pack(side = tk.LEFT, expand = False, fill = tk.Y)

        self.entry = tk.Entry(self, width = entry_width, relief = tk.RAISED)
        self.entry.pack(side = tk.LEFT, expand = True)

    def change_entry(self, text):
        self.entry.delete(0,tk.END)
        self.entry.insert(0,text)

    def get(self):
        return self.entry.get()
    
    def clear(self):
        self.entry.delete(0, tk.END)

# Checkbox
class Remarks(tk.Frame):
    def __init__(self, parent, text, **kwargs):
        tk.Frame.__init__(self, parent, kwargs)
        self.label = tk.Label(self, text = text, font = 'Helvetica 10 bold', bg = self["background"], anchor='ne')
        self.label.pack(side = tk.LEFT, expand = True, fill = tk.Y)

        
        self.scroll = tk.Scrollbar(self)
        self.text = tk.Text(self, height = 3, relief = tk.RAISED, width = 100)
        self.scroll.pack(side = tk.RIGHT, fill = tk.Y)
        self.text.pack(side = tk.LEFT, fill = tk.BOTH)
        self.scroll.config(command = self.text.yview)
        self.text.config(yscrollcommand = self.scroll.set)
    
    def clear(self):
        self.text.delete(1.0, tk.END)

        

class Checkbox(tk.Frame):

    def onEnter(self, event):
        self.button.configure(bg = 'gray76')
        
    def onLeave(self, event):
        self.button.configure(bg = self["background"])

    def changeState(self):
        self.state = not self.state

        if self.state:
            self.button.configure(image = self.on_img)
        else:
            self.button.configure(image = self.off_img)

    def __init__(self, text, parent, on_img, off_img, changeable = True, **kwargs):
        self.state = True
        self.on_img = on_img
        self.off_img = off_img
        tk.Frame.__init__(self, parent, kwargs, relief = tk.GROOVE)

        if not changeable:
            self.configure(bg = 'pale green')
            
       
        

        self.text = tk.Label(self, text = text, bg = self["background"], anchor='w')
        self.text.pack(side = tk.LEFT, expand = True, fill = tk.X)

        self.button = tk.Button(self,  relief = tk.FLAT, bg = self["background"], command = self.changeState, image = on_img)
        self.button.pack(side = tk.RIGHT)

        if not changeable:
            self.button.configure(state = tk.DISABLED)
        else:
            self.button.bind("<Enter>", self.onEnter)
            self.button.bind("<Leave>", self.onLeave)
    
    def clear(self):
        if not self.state:
            self.changeState()
    
# Entry with placeholder

class PlaceholderEntry(tk.Entry):
    def foc_in(self, event):
        if self.get() == self.placeholder :
            self.configure(fg = 'black')
            self.delete(0, tk.END)

    def foc_out(self, event):
        if self.get() == '':
            self.configure(fg = 'gray25')
            self.insert(0, self.placeholder)

    def __init__(self, parent, placeholder, **kwargs):

        tk.Entry.__init__(self, parent, kwargs, fg = 'gray25')

        self.placeholder = placeholder
        
        self.insert(0, self.placeholder)
        self.bind("<FocusIn>", self.foc_in)
        self.bind('<FocusOut>', self.foc_out)
        

    def get_data(self):
        data = tk.Entry.get(self)
        if(data == self.placeholder):
            return ''
        else:
            return data

# Class for password Entry
class PasswordEntry(tk.Entry):
    def foc_in(self, event):
        if self.get() == self.placeholder :
            self.configure(show = '*', fg = 'black')
            self.delete(0, tk.END)

    def foc_out(self, event):
        if self.get() == '':
            self.configure(show = '', fg = 'gray25')
            self.insert(0, self.placeholder)

    def __init__(self, parent, placeholder, **kwargs):

        tk.Entry.__init__(self, parent, kwargs, fg = 'gray25')

        self.placeholder = placeholder

        self.insert(0, self.placeholder)
        self.bind("<FocusIn>", self.foc_in)
        self.bind('<FocusOut>', self.foc_out)
    
    def get_data(self):
        data = tk.Entry.get(self)
        if(data == self.placeholder):
            return ''
        else:
            return data

# Class for set of multiple addable widgets
class PlusEntryFrame(tk.Frame):
    def __init__(self, parent, entry_name,  widget_class, widget_params, **kwargs):
        tk.Frame.__init__(self, parent, kwargs)
        widget_params['parent'] = self
        
        self.entries  = []
        self.widget_class = widget_class
        self.widget_params = widget_params
        entry = widget_class(**widget_params)
        entry.pack(side = tk.TOP, pady = 5)
        self.entries.append(entry)

        self.addBtn = tk.Button(self, bg  = self['background'], fg = 'white', text = "+ Add another {}".format(entry_name), relief = tk.FLAT, command = self.add_entry )
        self.addBtn.pack(side = tk.BOTTOM)
    
    def add_entry(self):
        entry = self.widget_class(**self.widget_params)
        entry.pack(side = tk.TOP, pady = 5)
        self.entries.append(entry)

    def get_data(self): # only if widget class has method get_data
        data = []
        for entry in self.entries:
            data.append(entry.get_data())
        return data
