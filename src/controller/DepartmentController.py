from src.model.repository.DepartmentRespository import DepartmentRespository
from src.service.DepartmentService import DepartmentService


class DepartmentController:
    def __init__(self):
        self.service = DepartmentRespository()

    def getAll(self):
       return self.service.findAll()

    def getById(self, ma_phong):
        return self.service.findById(ma_phong)

    def save(self,department):
        self.service.save(department)

    def delete(self,department):
        self.service.delete(department)

    def search(self, search_text,keyword):
        return self.service.search(search_text,keyword)


