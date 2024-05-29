import re
from loggerFile import logger
import logging
import os
import json

logger = logging.getLogger('loggerFile')

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
    def username(self, new_username: str) -> None:
        if new_username != self.__username:
            logger.info(f'Username changed from {self.__username} to {new_username}')
            self.__username = new_username

    @property
    def password(self) -> str:
        return self.__password

    @password.setter
    def password(self, new_password: str) -> None:
        if new_password != self.__password:
            logger.info(f'Password changed for user {self.__username}')
            self.__password = new_password

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, new_email: str) -> None:
        if new_email != self.__email:
            logger.info(f'Email changed for user {self.__username} to {new_email}')
            self.__email = new_email

    @property
    def enabled(self):
        return self.__enabled

    @enabled.setter
    def enabled(self, new_enabled: bool) -> None:
        if new_enabled != self.__enabled:
            logger.info(f'User {self.__username} enabled status changed to {new_enabled}')
            self.__enabled = new_enabled

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
                json.dump(base_dict, file,indent=2)

    @staticmethod
    def get_users() -> list:
        UserController.create_base_file()

        with open("users.json", "r") as file:
            users_data = json.load(file)["users"]
            users = [User(**user_data) for user_data in users_data]
            return users

    @staticmethod
    def save_users(users: list[User]):

        data = {"users": [user.get_dict() for user in users]}
        with open("users.json", "w") as file:
            json.dump(data, file)

    @staticmethod
    def add_user(user: User) -> bool:
        users = UserController.get_users()
        users.append(user)
        UserController.save_users(users)
        logger.info(f'User created: {user.username}')
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
            if user.username == info or user.email == info:
                return user

    @staticmethod
    def email_check(email: str) -> bool:
        pattern = r"^[a-zA-Z0-9.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$"

        return re.match(pattern, email) is not None

    @staticmethod
    def password_check(password: str) -> bool:
        return len(password) >= 8
