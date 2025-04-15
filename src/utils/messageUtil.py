from CTkMessagebox import CTkMessagebox

def show_info(message, title="Thông báo"):
    CTkMessagebox(title=title, message=message, icon="info")

def show_warning(message, title="Cảnh báo"):
    CTkMessagebox(title=title, message=message, icon="warning")

def show_error(message, title="Lỗi"):
    CTkMessagebox(title=title, message=message, icon="error")