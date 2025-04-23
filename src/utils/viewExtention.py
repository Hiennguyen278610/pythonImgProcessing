import cv2
import numpy as np
from PIL import Image
from customtkinter import CTkImage

def configFrame (radius=0):
    return {
        'corner_radius': radius,
        'width': 0,
        'height': 0
    }

def getCenterInit(frame, windowW, windowH):
    currentW = frame.winfo_screenwidth()
    currentH = frame.winfo_screenheight()

    x = (currentW - windowW) // 2
    y = (currentH - windowH) // 2
    return windowW, windowH, x, y

def cropImageToFitContainer(image_path, container_width, container_height):
    """
    Đọc ảnh từ đường dẫn, cắt từ trung tâm để phù hợp với tỉ lệ container
    và trả về một đối tượng CTkImage đã được resize
    
    Args:
        image_path (str): Đường dẫn đến file ảnh
        container_width (int): Chiều rộng của container
        container_height (int): Chiều cao của container
    
    Returns:
        CTkImage: Đối tượng CTkImage đã được xử lý
    """
    # Đọc ảnh với OpenCV
    original_img = cv2.imread(image_path)
    if original_img is None:
        raise ValueError(f"Không thể đọc ảnh từ đường dẫn: {image_path}")
    
    # Tính tỉ lệ khung chứa (height/width)
    container_ratio = container_height / container_width
    
    img_height, img_width = original_img.shape[:2]
    img_ratio = img_height / img_width
    
    if img_ratio < container_ratio:  # Ảnh quá rộng so với container
        # Tính chiều rộng mới sau khi cắt
        new_width = int(img_height / container_ratio)
        # Cắt từ giữa
        left_margin = (img_width - new_width) // 2
        cropped_img = original_img[:, left_margin:left_margin + new_width]
    else:  # Ảnh quá cao so với container
        # Tính chiều cao mới sau khi cắt
        new_height = int(img_width * container_ratio)
        # Cắt từ giữa
        top_margin = (img_height - new_height) // 2
        cropped_img = original_img[top_margin:top_margin + new_height, :]
    
    # Resize ảnh đã cắt để vừa với container
    resized_img = cv2.resize(cropped_img, (container_width, container_height))
    
    # Chuyển từ BGR (OpenCV) sang RGB (PIL)
    rgb_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB)
    
    # Chuyển thành đối tượng PIL Image
    pil_img = Image.fromarray(rgb_img)
    
    # Tạo CTkImage từ ảnh PIL
    return CTkImage(light_image=pil_img, size=(container_width, container_height))