from customtkinter import *
# from src.utils.viewExtention import configFrame

class DataTable(CTkScrollableFrame):
    def __init__(self, master, columns, rowSelectCallback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.scrollable = getattr(self, "_scrollbar", None) 
        self.scrollable.grid_remove()
        
        self.data = []
        self.columns = columns
        self.rowSelectCallback = rowSelectCallback
        self.selectedRow = None
        self.rowValue = None
        self.totalWidth = sum(col.get("width", 1) for col in self.columns)
        self.initHeader()

        self.rowValue = CTkFrame(self)
        self.rowValue.pack(fill="both", expand=True, padx=0, pady=0)
    
    def initHeader(self):
        headerFrame = CTkFrame(self)
        headerFrame.pack(fill="x", padx=0, pady=(0, 5))
        for i in range(self.totalWidth):
            headerFrame.grid_columnconfigure(i, weight=1)
        cnt = 0
        for col in self.columns:
            self.geneColumn(headerFrame, col, cnt)
            cnt += col.get("width", 1)
    
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
            for k in range(self.totalWidth):
                rowFrame.grid_columnconfigure(k, weight=1)
            cnt = 0
            for j, col in enumerate(self.columns):
                field = col.get("field", "")
                value = item.__dict__.get(field, "") if hasattr(item, field) else ""
                self.genecell(rowFrame, value, cnt, col.get("width", 1))
                cnt += col.get("width", 1)
            
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
            
    def geneColumn(self, headerFrame, col, current_col):
        header = CTkLabel(headerFrame, text=col.get("header", ""), font=("Arial", 12, "bold"), anchor="center")
        header.grid_propagate(False)
        header.grid(row=0, column=current_col, columnspan=col.get("width", 1), sticky="nsew", padx=5, pady=5)
        
    def genecell(self, rowFrame, value, current_col, colspan):
        cell = CTkLabel(rowFrame, text=str(value), anchor="center")
        cell.grid_propagate(False)
        cell.grid(row=0, column=current_col, columnspan=colspan, sticky="nsew", padx=5, pady=5)

    def getSelected(self):
        return self.selectedRow