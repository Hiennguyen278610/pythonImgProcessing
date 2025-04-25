from customtkinter import *
from datetime import datetime
from CTkMessagebox import CTkMessagebox
from PIL import Image
import os
from main import mainFrame
import FaceRecognition
from src.service.loginService import LoginService

import customtkinter
import calendar

from src.controller.DepartmentController import DepartmentController
from src.controller.EmployeeController import EmployeeController
from src.controller.PositionController import PositionController
from src.utils.viewExtention import getCenterInit
from src.controller.AttendanceController import AttendanceController

# Biến màu tối
primaryClr = "#6D54B5"
secondaryCrl = "#3C364C"  # Nền btn
accentClr = "#757283"  # Placeholder btn
bgClr = "#2c2736"
textClr = "#FFFFFF"
borderClr = "#000000"

# Image references dictionary to prevent garbage collection
imgReferences = {}


def safe_destroy(window):
    """Safely destroy a window, avoiding Tcl command errors."""
    # Nếu cửa sổ đã bị hủy rồi thì thôi
    if not window or not window.winfo_exists():
        return

    try:
        window.destroy()
    except Exception as e:
        # Bắt mọi lỗi liên quan đến Tcl và tiếp tục
        print(f"Error during safe_destroy: {e}")



# Center window function
def center_window(window, width, height):
    """Căn giữa cửa sổ trên màn hình desktop"""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = int((screen_width - width) / 2)
    y = int((screen_height - height) / 2)

    window.geometry(f"{width}x{height}+{x}+{y}")


# Hàm crop theo bottom ảnh
def bottomCrop(img, tempWidth, tempHeight, bias=0.7):
    w, h = img.size
    left = (w - tempWidth) // 2
    top = int((h - tempHeight) * bias)
    right = left + tempWidth
    bottom = top + tempHeight
    return img.crop((left, top, right, bottom))


# Simplified image loading function
def load_background_image(frame, label, image_path):
    """Load background image with better error handling"""
    global imgReferences

    # Check if image exists
    if not image_path or not os.path.exists(image_path):
        print(f"Image not found: {image_path}")
        # Configure label to show error text instead
        label.configure(text="Background Image Not Found", text_color="#FF6B6B")
        return False

    try:
        # Get frame dimensions
        width = frame.winfo_width()
        height = frame.winfo_height()

        # Wait until frame is properly sized
        if width <= 1 or height <= 1:
            return False

        # Load and process image
        img = Image.open(image_path)

        # Calculate ratios for proper cropping
        ratio = width / height
        img_ratio = img.width / img.height

        if img_ratio > ratio:
            crop_w = int(img.height * ratio)
            crop_h = img.height
        else:
            crop_w = img.width
            crop_h = int(img.width / ratio)

        # Crop the image
        img = bottomCrop(img, crop_w, crop_h)

        # Create CTkImage and explicitly store reference
        ctk_image = CTkImage(light_image=img, size=(width, height))
        imgReferences['background'] = ctk_image

        # Update label with image
        label.configure(image=ctk_image, text="")
        return True

    except Exception as e:
        print(f"Error loading background image: {e}")
        label.configure(text=f"Error loading image", text_color="#FF6B6B")
        return False


def find_background_image():
    """Find the background image file with proper paths"""
    # Start with the current script's directory
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Try common project structures
    possible_paths = [
        os.path.join(base_dir, "resources", "photo", "background.jpg"),
        os.path.join(base_dir, "Resources", "photo", "background.jpg"),
        os.path.join(os.path.dirname(base_dir), "resources", "photo", "background.jpg"),
        os.path.join(os.path.dirname(base_dir), "Resources", "photo", "background.jpg"),
        # Add absolute path as fallback (remove or adjust as needed)
        "/home/thanhhai/Documents/PYTHON/pythonImgProcessing/Resources/photo/background.jpg"
    ]

    # Add user's home directory as another possibility
    home_dir = os.path.expanduser("~")
    possible_paths.append(os.path.join(home_dir, "Documents", "PYTHON", "pythonImgProcessing",
                                       "Resources", "photo", "background.jpg"))

    # Check each path
    for path in possible_paths:
        if os.path.exists(path):
            print(f"Found background image at: {path}")
            return path

    # If not found, return None
    print("Background image not found in any of the expected locations.")
    return None


# Kiểm tra trường nhập có null hay không
def checknull(entries, loginPanel, loginService):
    nullEntry = [entry for entry in entries if not entry.get().strip()]
    if nullEntry:
        CTkMessagebox(title="Lỗi", message="Bạn cần phải điền đầy đủ thông tin")
    else:
        check, loginE = loginService.check_login(entries[0].get(), entries[1].get(), loginPanel)
        if check:
            CTkMessagebox(title="Thành công", message="Bạn đã đăng nhập thành công")

            # Store parent app reference
            parent_app = getattr(loginPanel, 'parent_app', None)

            # Use immediate execution instead of after
            try:
                safe_destroy(loginPanel)
                app = mainFrame()
                app.mainloop()
            except Exception as e:
                CTkMessagebox(title="Lỗi", message=f"Không thể mở giao diện chính: {str(e)}")
                # If error occurs, try to show parent app again
                if parent_app and parent_app.winfo_exists():
                    parent_app.deiconify()
        else:
            CTkMessagebox(title="Thất bại", message="Sai tài khoản hoặc mật khẩu")


# giao dien camera cho thang nhan vien
def staffPanel(loginPanel):
    FaceRecognition.App().mainloop()
    safe_destroy(loginPanel)


def loginFrame():
    loginPanel = CTk()
    # Configure before centering
    loginPanel.title("Đăng nhập")
    loginPanel._set_appearance_mode("light")
    loginPanel.configure(fg_color=textClr)

    # Store reference to parent app (will be set from Chamcong.py)
    loginPanel.parent_app = None

    # Center window immediately
    center_window(loginPanel, 1120, 630)

    loginS = LoginService()

    body = CTkFrame(loginPanel, fg_color=bgClr)
    body.place(relwidth=1, relheight=1)
    body.grid_rowconfigure(0, weight=1)
    body.grid_columnconfigure(0, weight=1)
    body.grid_columnconfigure(1, weight=1)

    left = CTkFrame(body)
    left.grid(row=0, column=0, sticky="nsew")

    right = CTkFrame(body, fg_color="transparent")
    right.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    right.grid_rowconfigure(0, weight=1)
    right.grid_columnconfigure(0, weight=1)

    innerRight = CTkFrame(right, fg_color=bgClr)
    innerRight.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    innerRight.grid_columnconfigure(0, weight=1)
    innerRight.grid_rowconfigure(0, weight=0)
    innerRight.grid_rowconfigure(1, weight=1)

    headRight = CTkFrame(innerRight, fg_color=bgClr)
    headRight.grid(row=0, column=0, padx=80, pady=10, sticky="w")

    title = CTkLabel(headRight,
                     text="Ứng dụng điểm danh",
                     text_color=textClr,
                     font=("San Serif", 36, "bold"))
    title.grid(row=0, column=0, padx=10, pady=5, sticky="w")

    slogan = CTkLabel(headRight,
                      text=f'Hôm nay là {datetime.now().strftime("%d/%m/%Y")}, bạn đã điểm danh chưa !!!',
                      text_color=accentClr,
                      font=("San Serif", 14, "bold"))
    slogan.grid(row=1, column=0, padx=10, pady=5, sticky="w")

    footRight = CTkFrame(innerRight, fg_color=bgClr)
    footRight.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    footRightFrame = CTkFrame(footRight, fg_color=bgClr)
    footRightFrame.place(relx=0.5, rely=0.4, anchor="center", relwidth=0.8, relheight=0.3)
    footRightFrame.grid_rowconfigure(0, weight=1, minsize=40)
    footRightFrame.grid_rowconfigure(1, weight=1, minsize=40)
    footRightFrame.grid_rowconfigure(2, weight=1)
    footRightFrame.grid_columnconfigure(0, weight=1)

    usernameTxt = CTkEntry(footRightFrame,
                           placeholder_text="Nhập username ....",
                           font=("San Serif", 14, "bold"),
                           border_width=0,
                           fg_color=secondaryCrl,
                           text_color=accentClr)
    usernameTxt.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

    passwordTxt = CTkEntry(footRightFrame,
                           placeholder_text="Nhập mật khẩu .....",
                           font=("San Serif", 14, "bold"),
                           border_width=0,
                           fg_color=secondaryCrl,
                           text_color=accentClr,
                           show="*")  # Hide password
    passwordTxt.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

    loginBtn = CTkButton(footRightFrame,
                         text="Đăng nhập",
                         font=("San Serif", 18, "bold"),
                         fg_color=primaryClr,
                         border_spacing=5,
                         command=lambda: checknull([usernameTxt, passwordTxt], loginPanel, loginS))
    loginBtn.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

    # Create image label
    imgLabel = CTkLabel(left, text="", image=None)
    imgLabel.place(relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=1)

    # Find background image with robust approach
    imgPath = find_background_image()
    if not imgPath:
        # Show warning and use solid color instead
        left.configure(fg_color="#3C364C")  # Use a solid color as fallback
        imgLabel.configure(text="Background Image Not Found")
    else:
        # Load the image when the window is properly initialized
        def delayed_load():
            if left.winfo_width() > 1:
                load_background_image(left, imgLabel, imgPath)
            else:
                # If still not ready, try again in 100ms
                loginPanel.after(100, delayed_load)

        # Start the delayed loading process
        loginPanel.after(300, delayed_load)

        # Handle resize events
        def on_resize(event):
            # Only update image if the widget still exists
            if left.winfo_exists() and imgLabel.winfo_exists():
                load_background_image(left, imgLabel, imgPath)

        # Bind resize event handler
        left.bind("<Configure>", on_resize)

    # Define what happens when the window's close button is clicked
    def on_close():
        try:
            # If there's a parent app, show it again
            if hasattr(loginPanel, 'parent_app') and loginPanel.parent_app and loginPanel.parent_app.winfo_exists():
                loginPanel.parent_app.deiconify()
                safe_destroy(loginPanel)
            else:
                # Return to main attendance screen
                safe_destroy(loginPanel)
                from Chamcong import HomeFrame

                root = CTk()
                root.withdraw()
                root.title("Hệ thống chấm công")
                root._set_appearance_mode("dark")

                home_frame = HomeFrame(root)
                home_frame.pack(fill="both", expand=True)

                center_window(root, 800, 600)
                root.deiconify()
                root.mainloop()
        except Exception as e:
            CTkMessagebox(
                title="Lỗi",
                message=f"Không thể quay lại màn hình chính: {str(e)}"
            )
            # If all else fails, just destroy the window
            safe_destroy(loginPanel)

    # Set the window close protocol
    loginPanel.protocol("WM_DELETE_WINDOW", on_close)

    return loginPanel


# Clean up resources on exit
def cleanup():
    global imgReferences
    imgReferences.clear()


import atexit

atexit.register(cleanup)

# Allow direct execution for testing
# if __name__ == "__main__":
#     loginFrame().mainloop()