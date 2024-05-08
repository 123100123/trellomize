class Project:
    def __init__(self, name, id, tasks, users, leader):
        self.__name = name
        self.__id = id
        self.__leader = leader
        self.__tasks = tasks if tasks else []
        self.__users = users if users else []

    @property
    def get_name(self):
        return self.__name

    @get_name.setter
    def set_name(self, new_name):
        self.__name = new_name

    @property
    def get_leader(self):
        return self.__leader

    @property
    def get_id(self):
        return self.__id

    @property
    def get_users(self):
        return self.__users

    def add_user(self, new_user):
        if new_user.username not in self.__users.username:
            self.__users.append(new_user)

    def remove_user(self, del_user):
        if del_user.username in self.__users.username:
            self.__users.remove(del_user)
        else:
            return False
