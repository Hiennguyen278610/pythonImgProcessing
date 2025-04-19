from src.model.repository.DepartmentRespository import DepartmentRespository


class DepartmentController:
    def __init__(self):
        self.repository = DepartmentRespository()

    def getAll(self):
       return self.repository.findAll()

    def getById(self, ma_phong):
        return self.repository.findById(ma_phong)

    def save(self,department):
        self.repository.save(department)

    def delete(self,department):
        self.repository.delete(department)

    def search(self, search_text):
        departments = self.repository.findAll()
        return [d for d in departments if search_text.lower() in (d.ten_phong or '').lower()]


