from tkinter import Tk, Frame, font as tkfont, Label, Scrollbar, Text, Toplevel

class TextEditor(Frame):
    """
    Text Editor frame for the program
    """
    def __init__(self, master=None, uid=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)
        self.uid = uid
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=0)
        self.rowconfigure(0,weight=1)
        
        self._text = Text(self)
        self._text.grid(row=0,column=0,sticky="nswe")
        font = tkfont.Font(font=self._text['font'])
        tab_size = font.measure('    ')
        self._text.configure(undo=True)
        self._text.config(tabs=tab_size)
        self._text.bind("<Control-y>", lambda event: self._text.edit_redo)
        self._text.bind("<Control-z>", lambda event: self._text.edit_undo)
        self._scrollbar = Scrollbar(self,command=self._text.yview)
        self._scrollbar.grid(row=0,column=1,sticky="ns",padx=(0,0))
        self._text.config(yscrollcommand=self._scrollbar.set)
    def get(self):
        return self._text.get("1.0","end")
    def insert(self, index, chars, *args):
        self._text.insert(index, chars, *args)

class TipWindow(Toplevel):
    """
    Window of the ToolTip
    """
    def __init__(self,coords,text):
        super().__init__()
        x,y = coords
        self.wm_geometry("+%d+%d" % (x, y))
        label = Label(self, text=text, justify='left',wraplength=200,
                      background="#ffffe0", relief='solid', borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)
        self.wm_overrideredirect(True)
        self.update()
               
class ToolTip:
    """
    Handling of the ToolTip
    """
    def __init__(self,widget,text):
        self.wd = None
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self._enter)
        self.widget.bind("<ButtonPress-1>", lambda event: [self._leave(event), self._click(event)])
        self.widget.bind("<Leave>", self._leave)
        
    def _enter(self,event=None):
        self._job = self.widget.after(1000,self._create)
        
    def _leave(self,event=None):
        self.widget.after_cancel(self._job)
        self._destroy()
           
    def _create(self):
        self.left=False
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        if not self.left:
            self.wd = TipWindow((x,y), self.text)

    def _destroy(self):
        self.left=True
        if self.wd:
            self.wd.destroy()
            self.wd = None
            
    def _click(self,event):
        if event.widget.winfo_class() == 'TMenubutton':
            submenu = event.widget.winfo_children()[0]
            # submenu.invoke(0)
        else:
            event.widget.invoke()
    
if __name__ == "__main__":
    root = Tk()
    text = TextEditor(root)
    text.pack(fill="both",expand=True)
    root.mainloop()