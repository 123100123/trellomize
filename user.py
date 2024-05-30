import re
from loggerFile import logger
import logging
import os
import json
from encoder import Encoder

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
        """
        Returns a dict of user attrs to be saved as json
        """
        dic = {
            "username": self.__username,
            "password": Encoder.encrypt(self.__password),
            "email": self.__email,
            "enabled": self.__enabled,
        }
        return dic


class UserController:
    @staticmethod
    def create_base_file() -> None:
        """
        creates user.json if it hasn't been created before
        """ 
        if not os.path.exists("users.json"):
            base_dict = {"users": []}
            with open("users.json", "w") as file:
                json.dump(base_dict, file,indent=2)

    @staticmethod
    def get_users() -> list[User]:
        """
        reads users.json and returns a list of all user objects
        """
        UserController.create_base_file()

        with open("users.json", "r") as file:
            users_data = json.load(file)["users"]
            for user_data in users_data:
                user_data["password"] = Encoder.decrypt(user_data["password"])
            users = [User(**user_data) for user_data in users_data]
            return users

    @staticmethod
    def save_users(users: list[User]) -> None:
        """
        saves user objects as json
        """
        data = {"users": [user.get_dict() for user in users]}
        with open("users.json", "w") as file:
            json.dump(data, file)
        

    @staticmethod
    def add_user(user: User) -> None:
        """
        saves a new user to the list of users
        """
        users = UserController.get_users()
        users.append(user)
        UserController.save_users(users)
        logger.info(f'User created: {user.username}')

    @staticmethod
    def remove_user(user: User) -> None:
        """
        removes a new user from the list of users
        """
        users = UserController.get_users()
        usernames = [_user.username for _user in users]
        if user.username not in usernames:
            return False
        users.pop(usernames.index(user.username))
        UserController.save_users(users)

    @staticmethod
    def exists(info: str) -> bool:
        """
        checks wether a user with the inputed arg exists in saved users
        """
        users = UserController.get_users()
        usernames = [_user.username for _user in users]
        emails = [_user.email for _user in users]

        return info in usernames or info in emails

    @staticmethod
    def upadate_user(user: User) -> None:
        """
        updates the entered user in the json file
        """
        users = UserController.get_users()
        for i, _user in enumerate(users):
            if _user.username == user.username:
                users[i] = user
                break
        
        UserController.save_users(users)

    @staticmethod
    def get_user(info: str) -> User:
        """
        returns the user with the inputed username/email
        """
        users: list[User] = UserController.get_users()
        for user in users:
            if user.username == info or user.email == info:
                return user

    @staticmethod
    def email_check(email: str) -> bool:
        """
        checks wether the email has the correct pattern or not
        """
        pattern = r"^[a-zA-Z0-9.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$"

        return re.match(pattern, email) is not None

    @staticmethod
    def password_check(password: str) -> bool:
        """
        checks if the input password is of correct form
        """
        return len(password) >= 8
