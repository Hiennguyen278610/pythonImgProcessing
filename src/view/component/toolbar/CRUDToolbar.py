import os
import io
from cairosvg import svg2png
from PIL import Image
import customtkinter
from customtkinter import CTkFrame, CTkButton, CTkImage
from src.view.colorVariable import *

# Configuration for button styling
configButton = {
    "fg_color": Midnight_Navy,
    "text_color": textClr,
    "border_color": borderClr,
    "border_width": 2,
    "width": 120,
    "height": 40,
}

class CRUDToolbar(CTkFrame):
    def __init__(self, master, addCallback=None, editCallback=None, deleteCallback=None, viewCallback=None, **kwargs):
        super().__init__(master, fg_color=Ocean_Blue, **kwargs)

        self.addCallback = addCallback
        self.editCallback = editCallback
        self.deleteCallback = deleteCallback
        self.viewCallback = viewCallback

        # Load SVG icons and convert to CTkImage
        self.icons = self._load_svg_icons([
            ('add', 'Thêm'),
            ('update', 'Sửa'),
            ('delete', 'Xóa'),
            ('detail', 'Chi tiết')
        ])

        # Configure grid
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Create buttons with icons
        self.addBtn = CTkButton(
            self,
            text="Thêm",
            image=self.icons['add'],
            compound="left",
            command=self.onAdd,
            **configButton
        )
        self.addBtn.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.editBtn = CTkButton(
            self,
            text="Sửa",
            image=self.icons['update'],
            compound="left",
            command=self.onEdit,
            **configButton
        )
        self.editBtn.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        self.deleteBtn = CTkButton(
            self,
            text="Xóa",
            image=self.icons['delete'],
            compound="left",
            command=self.onDelete,
            **configButton
        )
        self.deleteBtn.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")

        self.viewBtn = CTkButton(
            self,
            text="Chi tiết",
            image=self.icons['detail'],
            compound="left",
            command=self.onView,
            **configButton
        )
        self.viewBtn.grid(row=0, column=3, padx=5, pady=5, sticky="nsew")

        self.enableItemButtons(False)


    def _load_svg_icons(self, items, size=(20, 20)):

        icons = {}
        # Đặt đường dẫn đầy đủ đến thư mục Resources/svg
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

    def onAdd(self):
        if self.addCallback:
            self.addCallback()

    def onEdit(self):
        if self.editCallback:
            self.editCallback()

    def onDelete(self):
        if self.deleteCallback:
            self.deleteCallback()

    def onView(self):
        if self.viewCallback:
            self.viewCallback()

    def enableItemButtons(self, enable=True):
        state = "normal" if enable else "disabled"
        self.editBtn.configure(state=state)
        self.deleteBtn.configure(state=state)
        self.viewBtn.configure(state=state)
