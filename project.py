import json
import os
import datetime
from comment import Comment
import uuid

class Task:
    def __init__(
        self,
        name : str,
        state : str,
        starting_date : str,
        ending_date : str,
        description : str,
        users : list[str], 
        comments: list[Comment],
        priority : int,
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
        self.__name = new_name

    @property
    def state(self) -> str:
        return self.__state

    @state.setter
    def state(self, new_state: str) -> None:
        self.__state = new_state

    @property
    def starting_date(self) -> str:
        return self.__starting_date

    @starting_date.setter
    def starting_date(self, new_starting_date: str) -> None:
        self.__starting_date = new_starting_date

    @property
    def ending_date(self) -> str:
        return self.__ending_date

    @ending_date.setter
    def ending_date(self, new_ending_date: str) -> None:
        self.__ending_date = new_ending_date

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, new_description: str) -> None:
        self.__description = new_description

    @property
    def users(self) -> list:
        return self.__users

    @users.setter
    def users(self, new_users: list) -> None:
        self.__users = new_users

    @property
    def comments(self) -> list:
        return self.__comments
    
    def add_comment(self, user: str, task_id: str):
        text = input("Enter the comment text: ")
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        comments_file_path = f"Tasks/{task_id}/comments.txt"
        if not os.path.exists(comments_file_path):
            os.makedirs(os.path.dirname(comments_file_path), exist_ok=True)
            id = 1
        else:
            with open(comments_file_path, "r") as file:
                lines = file.readlines()
                if lines:
                    last_line = lines[-1]
                    id = int(last_line.split()[0]) + 1
                else:
                    id = 1
        with open(comments_file_path, "a") as file:
            file.write(f"{id} {user} {date} {text}\n")
        comment = Comment(text, date, user, id)
        self.__comments.append(comment)

    @property
    def priority(self) -> int:
        return self.__priority

    @priority.setter
    def priority(self, new_priority: int) -> None:
        self.__priority = new_priority
    
    def get_dict(self):
        dic = {
            "name": self.__name,
            "state": self.__state,
            "starting_date": self.__starting_date,
            "ending_date": self.__ending_date,
            "description": self.__description,
            "users": self.__users,
            "comments": [comment.__dict__ for comment in self.__comments],
            "priority": self.__priority,
        }
        return dic


class Project:
    def __init__(
        self,
        name: str,
        tasks: list[Task],
        users: list[str],
        leader: str,
    ) -> None:
        self.__name = name
        self.__id = str(uuid.uuid4())
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
    def tasks(self):
        return self.__tasks
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
    
    def get_task(self,task):
        _index = [_task.id for _task in self.__tasks].index(task.id)
        task = self.__tasks[_index]
        return task


    def add_task(self, task) -> bool:
        if task not in self.__tasks:
            self.__tasks.append(task)
            return True
        else :
            return False

    def remove_task(self, task) -> bool:
        if task in self.__tasks:
            self.__tasks.remove(task)
            return True
        else :
            return False

    def get_dict(self):
        dic = {
            "name": self.__name,
            "id": self.__id,
            "tasks": [task.get_dict() for task in self.__tasks],
            "users": self.__users,
            "leader": self.__leader
        }
        return dic


class ProjectController:
    @staticmethod
    def create_base_file():
        if not os.path.exists("projects.json"):
            base_dict = {"projects": []}
            with open("projects.json", "w") as file:
                json.dump(base_dict, file)

    @staticmethod
    def get_projects(username):
        ProjectController.create_base_file()
        "only returns the users' projects"
        projects = []
        with open("projects.json", "r") as file:
            data = json.load(file)
            projects_keywords = [{**project} for project in data["projects"]]
            for project_keywords in projects_keywords:
                if username not in project_keywords["users"]:
                    continue
                tasks_data = project_keywords["tasks"]
                del project_keywords["tasks"]
                
                # Create Task objects correctly
                tasks = [Task(
                    name=task_data['name'],
                    state=task_data['state'],
                    starting_date=task_data['starting_date'],
                    ending_date=task_data['ending_date'],
                    description=task_data['description'],
                    users=task_data['users'],
                    comments=[Comment(**comment_data) for comment_data in task_data['comments']],
                    priority=task_data['priority']
                ) for task_data in tasks_data]
                
                project_keywords["tasks"] = tasks
                projects.append(Project(**project_keywords))
        return projects

    @staticmethod
    def save_projects(projects):
        with open("projects.json", "w") as file:
            data = {"projects": [project.get_dict() for project in projects]}
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
        projects.append(project)
        ProjectController.save_projects()

    @staticmethod
    def get_project(project_id):
        projects = ProjectController.get_projects()
        project_ids = [project.id for project in projects]
        if project_id not in project_ids:
            return None

        return projects
    
    @staticmethod
    def exists(name):
        projects = ProjectController.get_projects()
        return any(project.name == name for project in projects)
    