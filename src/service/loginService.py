from src.model.repository.loginRepository import LoginRepository
from src.model.entity.loginEntity import LoginEntity

class LoginService:
    def __init__(self):
        self.loginR = LoginRepository()

    def check_login(self, username, password, loginPanel):
        check, loginEntity = self.loginR.check_login(username, password, loginPanel)
        if check and loginEntity:
            return True, loginEntity
        return False, None
