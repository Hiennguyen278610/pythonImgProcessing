from customtkinter import CTkScrollableFrame, CTkButton
from src.view.colorVariable import *

class TaskButton(CTkButton):
    """Button tùy chỉnh cho TaskBar"""
    def __init__(self, master, text, key, command=None, **kwargs):
        super().__init__(
            master, 
            text=text, 
            command=command,
            fg_color=secondaryCrl,
            hover_color=accentClr,
            text_color=textClr,
            corner_radius=8,
            height=40,
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
        
        self.grid_columnconfigure(0, weight=1)
    
    def add_entity(self, name, key, entity_class=None):
        """Thêm một đối tượng vào thanh tác vụ"""
        # Lưu thông tin đối tượng
        self.entities.append({
            "name": name,
            "key": key,
            "entity_class": entity_class
        })
        
        # Tạo nút cho đối tượng
        button = TaskButton(
            self,
            text=name,
            key=key,
            command=lambda k=key: self.select_entity(k)
        )
        button.grid(row=len(self.entities)-1, column=0, padx=10, pady=5, sticky="ew")
        self.buttons[key] = button
    
    def select_entity(self, key):
        """Chọn một đối tượng và kích hoạt callback"""
        if self.selected_key:
            # Trả về style cũ cho nút trước đó
            self.buttons[self.selected_key].configure(fg_color=secondaryCrl)
        
        # Đánh dấu nút mới được chọn
        self.selected_key = key
        self.buttons[key].configure(fg_color=accentClr)
        
        # Gọi callback với key được chọn
        if self.entity_callback:
            entity_info = next((e for e in self.entities if e["key"] == key), None)
            self.entity_callback(key, entity_info["entity_class"] if entity_info else None)