from user import User
import pandas as pd
from typing import Union
import os
import re
from encoder import Encoder


# all the data saving and reading should be encrypted in future
class UserController:
    def __init__(self) -> None:
        if not os.path.exists("users.csv"):
            self.__df = pd.DataFrame(
                columns=["username", "password", "email", "enabled"]
            )
            self.__save()
        else:
            self.__df = pd.read_csv("users.csv")
        self.__encoder = Encoder()
        pass

    def __save(self):
        self.__df.to_csv("users.csv", index=False)

    def exists(self, username: str) -> bool:
        """checks if a username exists

        Args:
            username (str)

        Returns:
            bool
        """
        return any(self.__df["username"] == username)

    def add_user(self, user: User) -> bool:
        """
        Args:
            user (User)

        Returns:
            bool: result
        """
        if self.exists(user.username):
            return False

        new_row = pd.DataFrame(
            [[user.username, user.password, user.email, True]],
            columns=self.__df.columns,
        )
        self.__df = pd.concat([self.__df, new_row], ignore_index=True)

        self.__save()
        return True

    def remove_user(self, username: str) -> bool:
        """removes the user with a certain username

        Args:
            username (str)

        Returns:
            bool
        """
        if not self.exists(username):
            return False
        self.__df = self.__df.drop(self.__df[self.__df["username"] == username].index)
        self.__save()
        return True

    @staticmethod
    def is_email(email: str) -> bool:
        pattern = r"^[a-zA-Z0-9.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email) is not None

    def get_user(self, username: str) -> Union[User, None]:
        """
        Args:
            username (str)

        Returns:
            Union[User,None]
        """
        if not self.exists(username):
            return None

        data = self.__df[self.__df["username"] == username].iloc[0]
        user = User(
            data["username"],
            data["password"],
            data["email"],
            bool(data["enabled"]),
        )
        return user

    def get_users(self) -> Union[list, None]:
        """returns a list of all the users

        Returns:
            list[User]
        """
        users = []
        for _, data in self.__df.iterrows():
            user = User(
                data["username"],
                data["password"],
                data["email"],
                bool(data["enabled"]),
            )
            users.append(user)
        if users == []:
            return None
        return users
    
    def disable_user(self,username:str)->bool:
        if not self.exists(username):
            return False
        
        data = self.__df.index[self.__df['username'] == username].tolist()[0]
        
        self.__df.at[data, 'enabled'] = False
        self.__save()
    
    def enable_user(self,username:str)->bool:
        if not self.exists(username):
            return False
        
        data = self.__df.index[self.__df['username'] == username].tolist()[0]
        
        self.__df.at[data, 'enabled'] = True
        
        self.__save()
    
