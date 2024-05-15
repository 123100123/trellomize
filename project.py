import json
import os


class Task:
    def __init__(
        self,
        name,
        state,
        starting_date,
        ending_date,
        description,
        users,
        comments,
        priority,
    ) -> None:
        self.__name = name
        self.__state = state
        self.__starting_date = starting_date
        self.__ending_date = ending_date
        self.__description = description
        self.__users = users
        self.__comments = comments
        self.__priority = priority

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, new_name: str) -> bool:
        if ProjectController.exists(new_name):
            return False
        self.__name = new_name
        return True

    def get_dict(self):
        dic = {
            "name": self.__name,
            "state": self.__state,
            "starting_date": self.__starting_date,
            "ending_date": self.__ending_date,
            "description": self.__description,
            "users": self.__users,
            "comments": self.__comments,
            "priority": self.__priority,
        }
        return dic


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
        self.__tasks = tasks
        self.__users = users

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
        return False

    def remove_user(self, user: str) -> bool:
        if user in self.__users:
            self.__users.remove(user)
            return True
        return False

    def get_tasks(self):
        return self.__tasks

    def add_task(self, task):
        # append the input task to the tasks list
        pass

    def remove(self, task):
        # remove the input task to the tasks list
        pass

    def get_dict(self):
        dic = {
            "name": self.__name,
            "id": self.__id,
            "tasks": [task.get_dict() for task in self.__tasks],
            "users": self.__users,
            "leader": self.__leader,
        }
        return dic


class ProjectController:
    def create_base_file():
        if not os.path.exists("projects.json"):
            base_dict = {"projects": []}
            with open("projects.json", "w") as file:
                json.dump(base_dict, file)

    @staticmethod
    def get_projects():
        ProjectController.create_base_file
        projects = []
        with open("projects.json", "r") as file:
            data = json.load(file)
            projects_keywords = [{**project} for project in data["projects"]]
            for project_keywords in projects_keywords:
                tasks_data = project_keywords["tasks"]
                del project_keywords["tasks"]
                tasks = [Task(**task_data) for task_data in tasks_data]
                project_keywords["tasks"] = tasks

                projects.append(Project(**project_keywords))

        return projects

    @staticmethod
    def save_projects(projects):
        with open("projects.json", "w") as file:
            data = {"projects": [project.get_dict() for project in projects]}
            print(data)
            json.dump(data, file)

    @staticmethod
    def add_project(project):
        projects = ProjectController.get_projects()
        projects.append(project)
        ProjectController.save_projects(projects)

    @staticmethod
    def remove_project(project):
        projects = ProjectController.get_projects()
        projects.remove(project)
        ProjectController.save_projects(projects)

    @staticmethod
    def update_project(project):
        projects = ProjectController.get_projects()
        ids = [_project.id for _project in projects]
        projects.pop(ids.index(project.id))
        ProjectController.save_projects()

    @staticmethod
    def get_project(project_id):
        projects = ProjectController.get_projects()
        project_ids = [project.id for project in projects]
        if project_id not in project_ids:
            return None

        return projects
