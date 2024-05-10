from user import UserController
from user import User
class Project:
    def __init__(
        self,
        name: str,
        id: str,
        tasks: list[str],
        users: list[str],
        leader: str,
    ) -> None:
        self.__name = name
        self.__id = id
        self.__leader = leader
        self.__tasks = tasks if tasks else []
        self.__users = users if users else []

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, new_name: str) -> None:
        self.__name = new_name

    @property
    def leader(self) -> str:
        return self.__leader

    @property
    def id(self) -> str:
        return self.__id

    @property
    def users(self) -> list[str]:
        return [user.username for user in UserController.get_users()]

    def add_user(self, new_user: User) -> bool:
        return UserController.add_user(new_user)

    def remove_user(self, del_user: User) -> bool:
        return UserController.remove_user(del_user)

    def get_dict(self) -> dict:
        dic = {
            "name": self.name,
            "id": self.id,
            "leader": self.leader,
            "tasks": self.__tasks,
            "users": [user.get_dict() for user in UserController.get_users()],
        }
        return dic

