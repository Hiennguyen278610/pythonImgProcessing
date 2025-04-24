from datetime import date, datetime

def convertToDate (day):
    if not day:
        print ('Không nhận được tham số đầu vào')
        return None
    
    try: 
        if isinstance(day, str):
            return date.fromisoformat(day)
        elif isinstance(day, datetime):
            return day.date()
        elif isinstance(day, date):
            return day
        else:
            raise ValueError("Unsupported type")
    except ValueError:
        print(f"[Lỗi] Định dạng ngày đang được truyền vào là: {day}")
        pass
    
    return None


def convertDataComboBox (list, str1, str2):
        fullData = [vars(pos) for pos in list]
        keymap = { pos[str1]: pos[str2] for pos in fullData }
        return keymap
    