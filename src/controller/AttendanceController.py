import cv2
import customtkinter
from PIL import Image, ImageDraw
from customtkinter import CTkImage
from src.service.AttendanceService import AttendanceService

class AttendanceController:
    def __init__(self):
        self.service = AttendanceService()

    def attendance(self, frame):
        return self.service.get_employee_attendance(frame)

    def getLocation(self, frame):
        return self.service.locationFace(frame)

    def loadData(self):
        self.service.load_known_faces()

    def checkIn(self, frame, ma_nhan_vien):
        self.service.checkIn(frame, ma_nhan_vien)