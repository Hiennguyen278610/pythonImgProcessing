from customtkinter import *

def getCenterInit(frame, windowW, windowH):
    currentW = frame.winfo_screenwidth()
    currentH = frame.winfo_screenheight()

    x = (currentW - windowW) // 2
    y = (currentH - windowH) // 2
    return windowW, windowH, x, y