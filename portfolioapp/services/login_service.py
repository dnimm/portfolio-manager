from db import data_store
from domain.User import User

class LoginService:
    def __init__(self):
        self.current_user = None
    
    def login(self, username: str, password: str) -> bool:
        user = data_store.get_user(username)
        if user and user.password == password:
            self.current_user = user
            return True
        return False
    
    def logout(self):
        self.current_user = None
    
    def get_current_user(self):
        return self.current_user
    
    def is_admin(self):
        return self.current_user and self.current_user.is_admin