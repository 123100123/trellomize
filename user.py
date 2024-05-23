import re
import os
import json
from project import ProjectController, Project,Task


class User:
    def __init__(self, username: str, password: str, email: str, enabled: bool) -> None:
        self.__username = username
        self.__password = password
        self.__email = email
        self.__enabled = enabled

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

    def add_project(self, project: Project) -> None:
        self.__projects.append(project.id)
        ProjectController.add_project(self.__username, project)

    def remove_project(self, project: Project) -> None:
        self.__projects.remove(self.__username, project.id)
        ProjectController.remove_project(self.__username, project)

    def get_dict(self) -> dict:
        dic = {
            "username": self.__username,
            "password": self.__password,
            "email": self.__email,
            "enabled": self.__enabled,
        }
        return dic


# all the data saving and reading should be encrypted in future
class UserController:
    @staticmethod
    def create_base_file():
        if not os.path.exists("users.json"):
            base_dict = {"users": []}
            with open("users.json", "w") as file:
                json.dump(base_dict, file)

    @staticmethod
    def get_users() -> list:
        UserController.create_base_file()

        with open("users.json", "r") as file:
            users_data = json.load(file)["users"]

            # users = []
            # for user_data in users_data:

            #     user_data["projects"] = ProjectController.get_projects(
            #         user_data["username"]
            #     )
            #     users.append(User(**user_data))
            users = [User(**user_data) for user_data in users_data]
            return users

    @staticmethod
    def save_users(users: list[User]):

        data = {"users": [user.get_dict() for user in users]}
        for user_info in data["users"]:
            user_info["projects"] = [_project.id for _project in user_info["projects"]]
        with open("users.json", "w") as file:
            json.dump(data, file)

    @staticmethod
    def add_user(user: User) -> bool:
        users = UserController.get_users()
        users.append(user)
        UserController.save_users(users)
        return True

    @staticmethod
    def remove_user(user: User) -> bool:
        users = UserController.get_users()
        usernames = [_user.username for _user in users]
        if user.username not in usernames:
            return False
        users.pop(usernames.index(user.username))
        UserController.save_users(users)
        return True

    @staticmethod
    def exists(info: str) -> bool:
        users = UserController.get_users()
        usernames = [_user.username for _user in users]
        emails = [_user.email for _user in users]

        return info in usernames or info in emails

    @staticmethod
    def upadate_user(user: str) -> bool:
        UserController.remove_user(user)
        UserController.add_user(user)

    @staticmethod
    def get_user(info: str) -> bool:
        users: list[User] = UserController.get_users()
        for user in users:
            if user.username == info or user.username == info:
                return user

    @staticmethod
    def email_check(email: str) -> bool:
        pattern = r"^[a-zA-Z0-9.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$"

        return re.match(pattern, email) is not None

    @staticmethod
    def password_check(password: str) -> bool:
        return len(password) >= 8
