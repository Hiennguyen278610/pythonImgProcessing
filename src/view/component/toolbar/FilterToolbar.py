from customtkinter import *
from src.view.colorVariable import *
import os
import io
from cairosvg import svg2png
from PIL import Image

configButton = {
    "fg_color": Midnight_Navy,
    "text_color": textClr,
    "border_color": borderClr,
    "border_width": 2,
}


class FilterToolbar(CTkFrame):
    def __init__(self, master,
                 searchFields: list[dict],   # ví dụ: [{"label":"Tên","field":"ho_ten"},{"label":"Mã phòng","field":"ma_phong"}]
                 searchCallback=None,
                 resetCallback=None,
                 **kwargs):
        fg_color = kwargs.pop("fg_color", Ocean_Blue)
        super().__init__(master, fg_color=Ocean_Blue, **kwargs)

        self.searchCallback = searchCallback
        self.resetCallback = resetCallback

        # Tạo biến cho OptionMenu
        labels = [f["label"] for f in searchFields]
        self.field_map = {f["label"]: f["field"] for f in searchFields}
        self.selected_label = StringVar(value=labels[0])

        # Load icons
        self.icons = self._load_svg_icons([
            ('search', 'Tìm kiếm'),
            ('reset', 'Đặt lại')
        ])


        self.grid_columnconfigure((0,1,2,3), weight=1)

        self.fieldMenu = CTkOptionMenu(self,
            values=labels,
            variable=self.selected_label,
            fg_color=Sky_Harbor,
        )
        self.fieldMenu.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.searchEntry = CTkEntry(self, placeholder_text="Nhập từ khoá…", **configButton)
        self.searchEntry.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        self.searchBtn = CTkButton(self,
                                  text="Tìm",
                                  image=self.icons['search'] if 'search' in self.icons else None,
                                  compound="left",
                                  command=self.onSearch,
                                  **configButton)
        self.searchBtn.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")

        self.resetBtn = CTkButton(self,
                                 text="Reset",
                                 image=self.icons['reset'] if 'reset' in self.icons else None,
                                 compound="left",
                                 command=self.onReset,
                                 **configButton)
        self.resetBtn.grid(row=0, column=3, padx=5, pady=5, sticky="nsew")

    def _load_svg_icons(self, items, size=(20, 20)):

        icons = {}
        base_dir = os.path.normpath(
            os.path.join(
                os.path.dirname(__file__),
                '..', '..', '..', '..',
                'Resources', 'svg'
            )
        )
        for name, _ in items:
            svg_path = os.path.join(base_dir, f"{name}.svg")
            if os.path.exists(svg_path):
                png_data = svg2png(url=svg_path)
                pil_img = Image.open(io.BytesIO(png_data))
                icons[name] = CTkImage(light_image=pil_img, size=size)
            else:
                icons[name] = None
        return icons

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