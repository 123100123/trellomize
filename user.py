from Controller import UserController

class User:
    def __init__(
        self,
        username: str,
        password: str,
        email: str,
        enabled: bool,
        projects: list[str],
    ) -> None:
        self.__username = username
        self.__password = password
        self.__email = email
        self.__enabled = enabled
        self.__projects = projects

    @property
    def username(self) -> str:
        return self.__username

    @username.setter
    def username(self, new_username: str) -> bool:
        if UserController.exists(new_username):
            return False
        self.__username = new_username
        return True
        

    @property
    def password(self) -> str:
        return self.__password

    @password.setter
    def password(self, new_password: str) -> bool:
        if not UserController.password_check(new_password):
            return False
        self.__password = new_password
        return True

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, new_email: str) -> bool:
        if not UserController.email_check(new_email):
            return False
        self.__email = new_email
        return True

    @property
    def enabled(self):
        return self.__enabled

    @enabled.setter
    def enabled(self, new_enabled: bool) -> None:
        self.__enabled = new_enabled

    @property
    def projects(self):
        return self.__projects

    def add_project(self, project_id: str) -> None:
        if project_id  in self.__projects:
            self.__projects.append(project_id)

    def remove_project(self, project_id: str) -> None:
        if project_id in self.__projects.id:
            self.__projects.remove(project_id)
    
    def get_dict(self) -> dict:
        dic = {
            "username" : self.username,
            "password" : self.password,
            "email" : self.email,
            "enabled" : self.enabled,
            "projects": self.projects
        }
        return dic
