from tkinter import Tk, ttk, Frame, PhotoImage

class ClosableTabs(ttk.Notebook):
    """A ttk Notebook with close buttons on each tab"""

    __initialized = False

    def __init__(self, master=None, **kw):
        if not self.__initialized:
            self.__initialize_custom_style()
            self.__inititialized = True

        kw["style"] = "ClosableTabs"
        ttk.Notebook.__init__(self, master, **kw)

        self._active = None

        self.bind("<ButtonPress-1>", self.on_close_press, True)
        self.bind("<ButtonRelease-1>", self.on_close_release)

    def on_close_press(self, event):
        """Called when the button is pressed over the close button"""

        element = self.identify(event.x, event.y)

        if "close" in element:
            index = self.index("@%d,%d" % (event.x, event.y))
            self.state(['pressed'])
            self._active = index
            return "break"
    
    def _close_tab(self,index):
        """Actually closes the tab when called en produces the necessary events"""
        self.event_generate("<<NotebookTabClosing>>",x=index)
        child = self.winfo_children()[index]
        child.destroy()
        self.event_generate("<<NotebookTabClosed>>")
        
    def on_close_release(self, event):
        """Called when the button is released"""
        if not self.instate(['pressed']):
            return

        element =  self.identify(event.x, event.y)
        if "close" not in element:
            # user moved the mouse off of the close button
            self.state(["!pressed"])
            return

        index = self.index("@%d,%d" % (event.x, event.y))

        if self._active == index:
            self._close_tab(index)

        self.state(["!pressed"])
        self._active = None

    def __initialize_custom_style(self):
        style = ttk.Style()
        self.images = (
            PhotoImage("img_close", data='''
                R0lGODlhCAAIAMIBAAAAADs7O4+Pj9nZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
                '''),
            PhotoImage("img_closeactive", data='''
                R0lGODlhCAAIAMIEAAAAAP/SAP/bNNnZ2cbGxsbGxsbGxsbGxiH5BAEKAAQALAAA
                AAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU5kEJADs=
                '''),
            PhotoImage("img_closepressed", data='''
                R0lGODlhCAAIAMIEAAAAAOUqKv9mZtnZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
            ''')
        )

        style.element_create("close", "image", "img_close",
                            ("active", "pressed", "!disabled", "img_closepressed"),
                            ("active", "!disabled", "img_closeactive"), border=8, sticky='')
        style.layout("ClosableTabs", [("ClosableTabs.client", {"sticky": "nswe"})])
        style.layout("ClosableTabs.Tab", [
            ("ClosableTabs.tab", {
                "sticky": "nswe",
                "children": [
                    ("ClosableTabs.padding", {
                        "side": "top",
                        "sticky": "nswe",
                        "children": [
                            ("ClosableTabs.focus", {
                                "side": "top",
                                "sticky": "nswe",
                                "children": [
                                    ("ClosableTabs.label", {"side": "left", "sticky": ''}),
                                    ("ClosableTabs.close", {"side": "left", "sticky": ''}),
                                ]
                        })
                    ]
                })
            ]
        })
    ])

if __name__ == "__main__":
    root = Tk()

    notebook = ClosableTabs(width=200, height=200)
    notebook.pack(side="top", fill="both", expand=True)
    aap = notebook

    for color in ("red", "orange", "green", "blue", "violet"):
        frame = Frame(notebook, background=color)
        notebook.add(frame, text=color)
        
    def clicked():
        frame = Frame(notebook, background="black")
        notebook.add(frame, text="black") 
        
    but = ttk.Button(root,text="Click",command=clicked)
    but.pack(side="bottom")
            

    root.mainloop()