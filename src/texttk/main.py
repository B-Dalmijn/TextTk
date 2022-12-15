import os
import sys
from tkinter import (Tk, ttk, filedialog, Frame, 
    Menu, messagebox, PhotoImage, Text)

from tabs import ClosableTabs
from widgets import TextEditor, ToolTip

class texttk(Tk):
    def __init__(self):
        super().__init__()
        # Window properties
        self.title("TextTk")
        self.geometry("800x500")
        self.protocol("WM_DELETE_WINDOW" ,self._exit)
        self.logo = PhotoImage(file=os.path.join(os.path.dirname(os.path.abspath(__file__)),"resources\\icon.png"))
        # self.iconphoto(False,self.logo)
        self.tk.call("wm","iconphoto",self._w,self.logo)
        # self.eval('tk::PlaceWindow . center')
        
        # Initialize object variables
        self._untitled = 0
        self._cur = None
        self._state = True
        self._files = {}
        
        # Binds and config
        self.bind_all("<Control-n>", lambda event: self._new())
        self.bind_all("<Control-o>", lambda event: self._open())
        self.bind_all("<Control-s>", lambda event: self._save())
        self.bind_all("<Control-w>", lambda event: self._close())
        self.bind("<<DocModified>>",lambda event: self._modified_state())
        self.bind("<<DocSaved>>",lambda event: self._saved_state())
        
        # Main menubar
        menu = Menu(self,borderwidth=0)
        self.config(menu=menu)
        file_menu = Menu(menu,tearoff=0) 
        file_menu.add_command(label="New",command=self._new, accelerator="Ctrl+N")
        file_menu.add_separator()
        file_menu.add_command(label="Open",command=self._open, accelerator="Ctrl+O")
        file_menu.add_command(label="Save",command=self._save, accelerator="Ctrl+S")
        file_menu.add_command(label="Save as...",command=self._save_as)
        file_menu.add_command(label="Close",command=self._close, accelerator="Ctrl+W")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", accelerator="Alt+F4")
        menu.add_cascade(label='File',menu=file_menu)
        
        edit_menu = Menu(menu,tearoff=0)
        edit_menu.add_command(label="Preferences")
        menu.add_cascade(label='Edit',menu=edit_menu)
        self.columnconfigure(1,weight=1)
        # self.columnconfigure(2,weight=1)
        self.rowconfigure(0,weight=1)
        self._tree_frame = Frame(self)
        self._tabs = ClosableTabs(self)
        self._tabs.grid(row=0,column=1,sticky="nswe")
        self._tabs.bind("<<NotebookTabChanged>>", self._tab_id)
        self._tabs.bind("<<NotebookTabClosing>>",self._closing)
        self._tabs.bind("<<NotebookTabClosed>>", self._closed)
        
        self._pdf_frame = Frame(self)
        self._pdf_frame.grid(row=0,column=2,sticky="nswe")
        
    def _add(self,file):
        name = os.path.basename(file)
        text = TextEditor(self._tabs,uid=file)
        text.pack(expand=True,side="top",fill="both")
        text._text.bind("<<Modified>>", self._modified, True)
        self._tabs.add(text,text=name)
        self._tabs.select(text)
        self._files[file] = {"State":2,"Name":name,"Text":text}
            
    def _new(self):
        self._cur = f"Untitled {self._untitled}.txt"
        self._add(self._cur)
        self._untitled += 1
        
    def _open_from_file(self,file):
        self._add(file)
        self._files[file]["State"] = 2
        self._files[file]["Name"] = os.path.basename(file)
        self._files[file]["Text"].insert("1.0",self._read_file(file))
        self._files[file]["Text"]._text.edit_modified(False)        
    
    def _open(self):
        exts = [(f"{ext} files", f"*.{ext}") for ext in ["txt"]]
        file = filedialog.askopenfilename(parent=self,initialdir="",
                                          title="Select a file",
                                          filetypes=(*exts,("All", "*.*")))
        if file:
            if file in self._files:
                return
            self._open_from_file(file)
            
    def _read_file(self,file):
        with open(file,"r") as f:
            read = f.read()
        return read
    
    def _save(self):
        if self._files[self._cur]["State"] == 0:
            return self._save_as()
        else:
            return self._save_file(self._cur)
    
    def _save_as(self):
        exts = [(f".{ext} files", f"*.{ext}") for ext in ["txt"]]
        file = filedialog.asksaveasfilename(parent=self,initialdir="",
                                            title="Save as file",
                                            filetypes=(*exts,("All", "*.*")),
                                            defaultextension=exts[0])
        if file:
            self._files[file] = self._files.pop(self._cur)
            self._files[file]["State"] = 2
            self._files[file]["Name"] = os.path.basename(file)
            self._tabs.tab(self._index,text=os.path.basename(file))
            self._tabs.winfo_children()[self._index].uid = file
            self._cur = file
            return self._save_file(file)
        return False
    
    def _save_file(self,file):
        with open(file,"w") as f:
            f.write(self._files[self._cur]["Text"].get())
        self.event_generate("<<DocSaved>>")
        return True
    
    def _close(self):
        self._tabs._close_tab(self._index)
    
    def _closing(self,event):
        self._cur = self._tabs.winfo_children()[event.x].uid
        if self._files[self._cur]["State"] != 2:
            name = os.path.basename(self._cur)
            awnser = messagebox.askyesno("Save",f"Save: {name}? If not, changes will be lost.",default='yes')
            if awnser:
                self._save()
        del self._files[self._cur]
            
    def _closed(self,event):
        self._tab_id()
        if not self._tabs.tabs():
            self._new()
    
    def _exit(self):
        # awnser = messagebox.askyesno("Close program","Wish to close the program?",default='no')
        # if awnser:
        self._state = False
        self._index = 0
        for tab in self._tabs.tabs():
            self._close()
        self.destroy()

    def _modified(self,event):
        flag = event.widget.edit_modified()
        if flag:
            self.event_generate("<<DocModified>>")
        else:
            if self._files[self._cur]["State"] == 0:
                self._tabs.tab(self._index, text = self._files[self._cur]["Name"])
            else:
                self.event_generate("<<DocSaved>>")

    def _modified_state(self):
        name = self._files[self._cur]["Name"]
        if not self._files[self._cur]["State"] == 0:
            self._files[self._cur]["State"] = 1
        self._tabs.tab(self._index, text = name + "*")

    def _saved_state(self):
        self._files[self._cur]["Text"]._text.edit_modified(False)
        name = self._files[self._cur]["Name"]
        self._files[self._cur]["State"] = 2
        self._tabs.tab(self._index, text = name)

    def _tab_id(self,event=None):
        if self._tabs.tabs():
            self._index = self._tabs.index(self._tabs.select())
            self._cur = self._tabs.winfo_children()[self._index].uid
    
    def _del_widgets(self,parent):
        for widget in parent.winfo_children():
            widget.destroy()
    
def main():
    gui = texttk()
    try:  
        gui._open_from_file(sys.argv[1])
    except Exception:
        gui._new()
    gui.mainloop()
    
if __name__ == "__main__":
    main()   