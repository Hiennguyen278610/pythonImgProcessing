from customtkinter import CTkScrollableFrame, CTkButton, CTkImage
import os
import io
from cairosvg import svg2png
from PIL import Image
from src.view.colorVariable import *


class TaskButton(CTkButton):
    """Button tùy chỉnh cho TaskBar"""

    def __init__(self, master, text, key, icon=None, command=None, **kwargs):
        super().__init__(
            master,
            text=text,
            image=icon,
            compound="left" if icon else "none",
            command=command,
            fg_color=Ocean_Blue,
            hover_color=Midnight_Navy,
            text_color=textClr,
            corner_radius=8,
            height=50,
            **kwargs
        )

        self.key = key  # Key để xác định đối tượng


class TaskBar(CTkScrollableFrame):
    """Thanh chứa các nút điều hướng đến các đối tượng khác nhau"""

    def __init__(self, master, entity_callback=None, **kwargs):
        super().__init__(master, **kwargs)

        self.scrollable = getattr(self, "_scrollbar", None)
        self.scrollable.grid_remove()
        self.entity_callback = entity_callback  # Callback khi nhấn nút đối tượng
        self.entities = []  # Danh sách đối tượng
        self.buttons = {}  # Lưu trữ các nút theo key
        self.selected_key = None  # Key của nút đang được chọn
        self.icons = self._load_svg_icons([
            ('employee', 'Nhân viên'),
            ('contract', 'Hợp đồng'),
            ('position', 'Chức vụ'),
            ('department', 'Phòng ban'),
            ('attendance', 'Điểm danh')
        ])

        self.grid_columnconfigure(0, weight=1)

    def _load_svg_icons(self, items, size=(20, 20)):
        icons = {}

        base_dir = os.path.normpath(
            os.path.join(
                os.path.dirname(__file__),
                '..', '..', '..',
                'Resources', 'svg'
            )
        )


        if not os.path.exists(base_dir):
            print(f"Thư mục SVG không tồn tại: {base_dir}")
            return icons

        for name, _ in items:
            svg_path = os.path.join(base_dir, f"{name}.svg")
            if os.path.exists(svg_path):
                try:
                    png_data = svg2png(url=svg_path)
                    pil_img = Image.open(io.BytesIO(png_data))
                    icons[name] = CTkImage(light_image=pil_img, size=size)
                    print(f"Đã tải thành công icon: {name}")
                except Exception as e:
                    print(f" Không thể chuyển đổi SVG {name}: {str(e)}")
            else:
                icons[name] = None
        return icons

    def add_entity(self, name, key, entity_class=None):
        """Thêm một đối tượng vào thanh tác vụ"""
        # Lưu thông tin đối tượng
        self.entities.append({
            "name": name,
            "key": key,
            "entity_class": entity_class
        })

        # Lấy icon tương ứng với key (nếu có)
        icon = self.icons.get(key)

        # Tạo nút cho đối tượng
        button = TaskButton(
            self,
            text=name,
            key=key,
            icon=icon,
            command=lambda k=key: self.select_entity(k),
            anchor = "w",
            width=200
        )
        button.grid(row=len(self.entities) - 1, column=0, padx=10, pady=5, sticky="ew")
        self.buttons[key] = button

    def select_entity(self, key):
        """Chọn một đối tượng và kích hoạt callback"""
        if self.selected_key:
            # Trả về style cũ cho nút trước đó
            self.buttons[self.selected_key].configure(fg_color=Ocean_Blue)

        # Đánh dấu nút mới được chọn
        self.selected_key = key
        self.buttons[key].configure(fg_color=Midnight_Navy)

        # Gọi callback với key được chọn
        if self.entity_callback:
            entity_info = next((e for e in self.entities if e["key"] == key), None)
            self.entity_callback(key, entity_info["entity_class"] if entity_info else None)