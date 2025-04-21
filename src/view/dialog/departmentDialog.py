from customtkinter import CTkToplevel, CTkLabel, CTkEntry, CTkButton
from src.model.entity.DepartmentEntity import Department

class DepartmentDialog(CTkToplevel):
    def __init__(self,parent,controller,department = None,view_only=False):
        super().__init__(parent)
        self.controller = controller
        self.department = department
        self.view_only = view_only

        if self.view_only:
            self.title("Xem thông tin phòng ban")
        elif self.department:
            self.title("Chỉnh sửa phòng ban")
        else:
            self.title("Thêm phòng ban")
        self.geometry("500x300")
        self.resizable(False,False)
        self.transient(parent)
        self.focus_set()
        self.init()

    def init(self):
        CTkLabel(self,text="Mã trưởng phòng: ").pack(pady = 5)
        self.ma_truong_phong = CTkEntry(self)
        self.ma_truong_phong.pack(pady = 5)

        CTkLabel(self,text="Tên phòng: ").pack(pady = 5)
        self.ten_phong = CTkEntry(self)
        self.ten_phong.pack(pady = 5)

        if self.department:
            self.ma_truong_phong.insert(0,self.department.ma_truong_phong or '')
            self.ten_phong.insert(0,self.department.ten_phong or '')
            if self.view_only:
                self.ma_truong_phong.configure(state="disabled")
                self.ten_phong.configure(state="disabled")


        if not self.view_only:
                CTkButton(self,text="Cập nhật",command=self.save).pack(pady = 10)
        CTkButton(self,text="thoát",command=self.destroy).pack(pady = 10)


    def save(self):
        ma_truong_phong = self.ma_truong_phong.get() or None
        ten_phong = self.ten_phong.get() or None
        ma_phong = self.department.ma_phong if self.department else None

        dpm = Department(ma_phong = ma_phong,ma_truong_phong=ma_truong_phong,ten_phong=ten_phong)
        self.controller.save(dpm)

        self.master.loadData()
        self.destroy()