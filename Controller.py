from user import User
import pandas as pd
from typing import Union
import os
import re
from encoder import Encoder
import json


# all the data saving and reading should be encrypted in future
class UserController:
    @staticmethod
    def create_base_file():
        if not os.path.exists("data.json"):
            base_dict = {"users": []}
            with open("data.json", "w") as file:
                json.dump(base_dict, file)

    @staticmethod
    def get_users() -> list:
        UserController.create_base_file()

        with open("data.json", "r") as file:
            users_data = json.load(file)["users"]
            users = [User(**user_data) for user_data in users_data]
            return users

    @staticmethod
    def save_users(users: list[User]):
        data = {"users": [user.get_dict() for user in users]}

        with open("data.json", "w") as file:
            json.dump(data, file)

    @staticmethod
    def add_user(user: User) -> bool:
        users = UserController.get_users()
        if UserController.exists(user.username):
            return False
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
    def exists(username: str) -> bool:
        users = UserController.get_users()
        usernames = [_user.username for _user in users]
        return username in usernames
    
    @staticmethod
    def upadate_user(user:str) -> bool:
        if not UserController.exists(user.username):
            return False
        UserController.remove_user(user)
        UserController.add_user(user)
    
    @staticmethod
    def email_check(email: str) -> bool:
        pattern = r"^[a-zA-Z0-9.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$"

        return re.match(pattern, email) is not None
    
    @staticmethod
    def password_check(password: str) -> bool:
        return len(password >= 8)
    