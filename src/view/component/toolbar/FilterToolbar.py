from customtkinter import CTkFrame, CTkEntry, CTkButton, CTkOptionMenu, StringVar

class FilterToolbar(CTkFrame):
    def __init__(self, master,
                 searchFields: list[dict],   # ví dụ: [{"label":"Tên","field":"ho_ten"},{"label":"Mã phòng","field":"ma_phong"}]
                 searchCallback=None,
                 resetCallback=None,
                 **kwargs):
        super().__init__(master, **kwargs)

        self.searchCallback = searchCallback
        self.resetCallback = resetCallback

        # Tạo biến cho OptionMenu
        labels = [f["label"] for f in searchFields]
        self.field_map = {f["label"]: f["field"] for f in searchFields}
        self.selected_label = StringVar(value=labels[0])

        # Layout: [OptionMenu] [Entry] [Search] [Reset]
        self.grid_columnconfigure((0,1,2,3), weight=1)

        self.fieldMenu = CTkOptionMenu(self,
            values=labels,
            variable=self.selected_label
        )
        self.fieldMenu.grid(row=0, column=0, padx=(0,5), pady=5, sticky="nsew")

        self.searchEntry = CTkEntry(self, placeholder_text="Nhập từ khoá…")
        self.searchEntry.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        self.searchBtn = CTkButton(self, text="Tìm", command=self.onSearch)
        self.searchBtn.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")

        self.resetBtn = CTkButton(self, text="Reset", command=self.onReset)
        self.resetBtn.grid(row=0, column=3, padx=(5,0), pady=5, sticky="nsew")

    def onSearch(self):
        query = self.searchEntry.get().strip()
        field_label = self.selected_label.get()
        field = self.field_map[field_label]
        if self.searchCallback:
            self.searchCallback(field, query)

    def onReset(self):
        self.searchEntry.delete(0, 'end')
        if self.resetCallback:
            self.resetCallback()
