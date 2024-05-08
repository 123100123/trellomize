class User:
    def __init__(self, username, password, email, enabled, projects) -> None:
        self.__username = username
        self.__password = password
        self.__email = email
        self.__enabled = enabled
        self.__projects = projects if projects else []

    @property
    def get_username(self):
        return self.__username

    @get_username.setter
    def set_username(self, new_username):
        self.__username = new_username

    @property
    def get_password(self):
        return self.__password

    @get_password.setter
    def set_password(self, new_password):
        self.__password = new_password

    @property
    def get_email(self):
        return self.__email

    @get_email.setter
    def set_email(self, new_email):
        self.__email = new_email

    @property
    def get_enabled(self):
        return self.__enabled

    @get_enabled.setter
    def set_enabled(self, new_enabled):
        self.__enabled = new_enabled

    @property
    def get_projects(self):
        return self.__projects

    def add_project(self, new_project):
        if new_project.id not in self.__projects.id:
            self.__projects.append(new_project)

    def remove_project(self, del_project):
        if del_project.id in self.__projects.id:
            self.__projects.remove(del_project)
        else:
            return False
