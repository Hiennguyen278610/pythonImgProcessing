from customtkinter import CTkFrame, CTkEntry, CTkButton

class FilterToolbar(CTkFrame):
    def __init__(self, master, searchCallback=None, resetCallback=None, **kwargs):
        self.searchCallback = searchCallback
        self.resetCallback = resetCallback
        super().__init__(master, **kwargs)
        
        self.grid_columnconfigure(0, weight=6)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        
        self.searchVar = ""
        self.searchEntry = CTkEntry(self, placeholder_text="Search...")
        self.searchEntry.grid(row=0, column=0, padx=(0,5), pady=5, sticky="nsew")

        self.searchBtn = CTkButton(self, text="Search", command=self.onSearch)
        self.searchBtn.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        
        self.resetBtn = CTkButton(self, text="Reset", command=self.onReset)
        self.resetBtn.grid(row=0, column=2, padx=(5,0), pady=5, sticky="nsew")
    
    def onSearch(self):
        query = self.searchEntry.get()
        if self.searchCallback:
            self.searchCallback(query)
    
    def onReset(self):
        self.searchEntry.delete(0, 'end')
        if self.resetCallback:
            self.resetCallback()