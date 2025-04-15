from customtkinter import *

class DataTable(CTkScrollableFrame):
    def __init__(self, master, columns, rowSelectCallback=None, **kwargs):
        super().__init__(master, **kwargs)
        
        self.data = []
        self.columns = columns
        self.rowSelectCallback = rowSelectCallback
        self.selectedRow = None
        self.rowValue = None
        self.initHeader()

        self.rowValue = CTkFrame(self)
        self.rowValue.pack(fill="both", expand=True, padx=0, pady=0)
    
    def initHeader(self):
        headerFrame = CTkFrame(self)
        headerFrame.pack(fill="x", padx=0, pady=(0, 5))
        for i, col in enumerate(self.columns):
            self.geneColumn(headerFrame, col, i)
    
    def updateDataTable(self, data):
        self.data = data
        self.selectedRow = None
        self.loadData()
    
    def loadData(self):
        if self.rowValue:
            for widget in self.rowValue.winfo_children():
                widget.destroy()
        
        for i, item in enumerate(self.data):
            rowFrame = CTkFrame(self.rowValue)
            rowFrame.pack(fill="x", padx=0, pady=(0, 2))
            # Cấu hình grid_columnconfigure cho từng cột
            for j, col in enumerate(self.columns):
                weight = col.get("width", 1)
                rowFrame.grid_columnconfigure(j, weight=weight)
                field = col.get("field", "")
                value = item.__dict__.get(field, "") if hasattr(item, field) else ""
                self.genecell(rowFrame, value, j)
            
            # Gắn sự kiện click
            rowFrame.bind("<Button-1>", lambda e, row=item, idx=i: self.onclickRow(row, idx))
            for child in rowFrame.winfo_children():
                child.bind("<Button-1>", lambda e, row=item, idx=i: self.onclickRow(row, idx))
    
    def onclickRow(self, row, idx):
        self.selectedRow = row
        for i, frame in enumerate(self.rowValue.winfo_children()):
            frame.configure(fg_color="#7D6CCB") if i == idx else frame.configure(fg_color='transparent')
        
        if self.rowSelectCallback:
            self.rowSelectCallback(row)
            
    def geneColumn(self, headerFrame, col, i):
        weight = col.get("width", 1)
        headerFrame.grid_columnconfigure(i, weight=weight)
        header = CTkLabel(headerFrame, text=col.get("header", ""), font=("Arial", 12, "bold"), anchor="center")
        header.grid(row=0, column=i, sticky="nsew", padx=5, pady=5)
        
    def genecell(self, rowFrame, value, j):
        cell = CTkLabel(rowFrame, text=str(value), anchor="center")
        cell.grid(row=0, column=j, sticky="nsew", padx=5, pady=5)

    def getSelected(self):
        return self.selectedRow