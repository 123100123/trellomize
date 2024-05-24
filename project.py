import json
import logging
import os
import datetime
import uuid
import datetime
import re
from enum import Enum

logger = logging.getLogger('loggerFile')

class Task:
    class State(Enum):
        BackLog = 1
        ToDo = 2
        Doing = 3
        Done = 4
        Archived = 5

    class Priority(Enum):
        Low = 1
        Medium = 2
        High = 3
        Critical = 4

    def __init__(
        self,
        id: str,
        name: str,
        state: str,
        priority: str,
        starting_date: str,
        ending_date: str,
        description: str,
        users: list[str],
    ) -> None:
        self.__name = name
        self.__id = id
        self.__state = self.State[state]
        self.__priority = self.Priority[priority]
        self.__starting_date = starting_date
        self.__ending_date = ending_date
        self.__description = description
        self.__users = users
    
    def create_base_file(self):
        tasks_dir = "tasks"
        task_dir = os.path.join(tasks_dir, self.__id)
                
        if not os.path.exists(task_dir):
            os.makedirs(task_dir, exist_ok=True)
    
    def manage_actions(self, username:str, action: str):
        self.create_base_file()
        history_change = f"{username}: {action}"
        logger_change = f"{username}: {action} in {self.__id} task"
        logger.info(logger_change)
        with open(f"tasks/{self.__id}/history.txt", "a+") as file:
            file.write(history_change+"\n")
        
            
    @staticmethod
    def generate_id() -> str:
        """
        returns a 5 character uuid
        """
        return str(uuid.uuid4())[:5]

    @staticmethod
    def check_date(first_date: str, second_date=None) -> bool:
        current = datetime.date.today()
        if second_date == None:
            try:
                inp = datetime.datetime.strptime(first_date, "%Y-%m-%d")
                return inp >= current
            except:
                return False

        try:
            inp = datetime.datetime.strptime(first_date, "%Y-%m-%d")
            inp2 = datetime.datetime.strptime(second_date, "%Y-%m-%d")

            return inp2 > inp
        except:
            return False

    @staticmethod
    def current_date() -> str:
        """
        Returns:
            str: today's date
        """
        return datetime.date.today().strftime("%Y-%m-%d")

    @staticmethod
    def default_ending_date() -> str:
        """
        Returns:
            str: tommorow's date
        """
        return str(datetime.date.today() + datetime.timedelta(days=1))

    @property
    def id(self):
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self,args) -> None:
        username,new_name = args
        self.manage_actions(username,f"changed name from {self.__name} to {new_name}")
        self.__name = new_name

    @property
    def state(self) -> State:
        return self.__state

    @state.setter
    def state(self, username:str ,new_state: State) -> None:
        self.manage_actions(username,f"changed name from {self.__state.name} to {new_state.name}")
        self.__state = new_state

    @property
    def starting_date(self) -> str:
        return self.__starting_date

    @starting_date.setter
    def starting_date(self,username :str , new_starting_date: str) -> None:
        self.manage_actions(username, f"starting date changed from {self.__starting_date} to {new_starting_date}")
        self.__starting_date = new_starting_date

    @property
    def ending_date(self) -> str:
        return self.__ending_date
    
    @ending_date.setter
    def ending_date(self, username:str , new_ending_date: str) -> None:
        self.manage_actions(username, f"End date changed from {self.__starting_date} to {new_ending_date}")
        self.__ending_date = new_ending_date

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, username:str ,new_description: str) -> None:
        self.manage_actions(username , f"description changed from {self.__starting_date} to {new_description}")
        self.__description = new_description

    @property
    def users(self) -> list:
        return self.__users

    @property
    def comments(self) -> list:
        return self.__comments
    
    def add_comment(self,username: str,text):
        self.create_base_file()
        date = self.current_date()
        
        with open(f"tasks/{self.__id}/comment.txt", "a+") as file:
            file.write(f"{username}({date}): {text}\n")
          
        self.manage_actions(username , f"Comment added to task {self.__id} -> {text}")
    
    @property
    def read_comments(self) -> str:
        try:
            with open(f"tasks/{self.__id}/comment.txt", 'r') as file:
                comments = file.read()
            
            return comments
        except FileNotFoundError:
            return "The file does not exist."
        
    @property
    def priority(self) -> int:
        return self.__priority

    @priority.setter
    def priority(self,username:str, new_priority: int) -> None:
        self.manage_actions(username , f"changed priority from {self.__priority} to {new_priority}")
        self.__priority = new_priority

    def add_user(self, adder_username :str ,username: str):
        self.__users.append(username)
        self.manage_actions(adder_username , f"added {username}")

    def remove_user(self, username: str):
        self.__users.remove(username)

    def get_dict(self):
        dic = {
            "id": self.__id,
            "name": self.__name,
            "state": self.__state.name,
            "priority": self.__priority.name,
            "starting_date": self.__starting_date,
            "ending_date": self.__ending_date,
            "description": self.__description,
            "users": self.__users,
        }
        return dic


class Project:
    def __init__(
        self, name: str, tasks: list[Task], users: list[str], leader: str, id: str
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
        self.__users.append(new_user)

    def remove_user(self, user: str) -> None:
            self.__users.remove(user)
            logger.info(f"{self.leader} removed user {user} from project {self.__id}")

    def get_task(self, task):
        _index = [_task.id for _task in self.__tasks].index(task.id)
        task = self.__tasks[_index]
        return task

    def add_task(self, task) -> None:
        self.__tasks.append(task)
        logger.info(f"{self.__leader} added {task.id} task")

    def remove_task(self, task) -> None:
        self.__tasks.remove(task)
        logger.info(f"{self.__leader} removed {task.id} task")

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
                tasks = [Task(**task_data) for task_data in tasks_data]
                project_keywords["tasks"] = tasks

                projects.append(Project(**project_keywords))
        return projects

    @staticmethod
    def save_projects(projects):
        with open("projects.json", "w") as file:
            data = {"projects": [project.get_dict() for project in projects]}
            json.dump(data, file)

    @staticmethod
    def add_project(username, project):
        projects = ProjectController.get_projects(username)
        projects.append(project)
        ProjectController.save_projects(projects)
        logger.info(f"Project created: {project.__name} with ID: {project.__id}")

    @staticmethod
    def remove_project(username, project):
        projects = ProjectController.get_projects(username)
        projects.remove(project)
        ProjectController.save_projects(projects)

    @staticmethod
    def update_project(username, project: Project):
        print(username)
        projects = ProjectController.get_projects(username)
        print(projects)

        ids = [_project.id for _project in projects]
        print(ids)
        projects.pop(ids.index(project.id))
        projects.append(project)
        ProjectController.save_projects(projects)

    @staticmethod
    def get_project(username, project_id):
        projects = ProjectController.get_projects(username)
        project_ids = [project.id for project in projects]
        if project_id not in project_ids:
            return None

        return projects

    @staticmethod
    def exists(name):
        projects = ProjectController.get_projects()
        return any(project.name == name for project in projects)
