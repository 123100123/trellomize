class Project:
    def __init__(
        self,
        name: str,
        id: str,
        tasks: list[Task],
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
    def name(self, new_name: str) -> bool:
        if ProjectController.exists(new_name):
            return False
        self.__name = new_name
        return True

    @property
    def leader(self) -> str:
        return self.__leader

    @property
    def id(self) -> str:
        return self.__id

    @property
    def users(self) -> list[str]:
        return self.__users

    def add_user(self, new_user: str) -> bool:
        if new_user not in self.__users:
            self.__users.append(new_user)
            return True
        else:
            return False

    def remove_user(self, del_user: str) -> bool:
        if del_user in self.__users:
            self.__users.remove(del_user)
            return True
        else:
            return False

    def get_dict(self) -> dict:
        dic = {
            "name": self.name,
            "id": self.id,
            "leader": self.leader,
            "tasks": [task.get_dict() for task in self.__tasks],
            "users": self.users,
        }
        return dic

