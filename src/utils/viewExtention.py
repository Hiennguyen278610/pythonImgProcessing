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