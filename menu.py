from user import UserController, User, ProjectController, Project, Task
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
import msvcrt


class Menu:
    console = Console()

    @staticmethod
    def getch():
        char = msvcrt.getch()
        if char == b"\x00":  # Arrow key prefix
            char += msvcrt.getch()
            if char == b"\x00H":
                return "up"
            elif char == b"\x00P":
                return "down"
        elif char == b"\r":  # Enter key
            return "enter"
        else:
            return char

    @classmethod
    def print_table(cls, header, data, selected_index):
        table = Table(width=100)
        table.add_column(header, justify="center")

        for i, item in enumerate(data):
            if i == selected_index:
                table.add_row(f"[bold cyan]> {item}[/bold cyan]")
            else:
                table.add_row(f"{item}")
        cls.console.print(table, justify="center")

    @classmethod
    def choose(cls, header, *options_list):
        values = []
        data = []
        for options in options_list:
            if isinstance(options, dict):
                values.extend(list(options.keys()))
                data.extend([f"{key}: {value}" for key, value in options.items()])
            elif isinstance(options, list):
                data.extend(options)
                values.extend(options)

        selected_index = 0
        while True:
            cls.console.clear()
            cls.print_table(
                header, data, selected_index
            )  # Passing the original options for printing
            key = cls.getch()

            if key == "up":
                selected_index = (selected_index - 1) % len(data)
            elif key == "down":
                selected_index = (selected_index + 1) % len(data)
            elif key == "enter":
                return values[selected_index]

    @classmethod
    def get_info(cls, description):
        cls.console.clear()
        return cls.console.input(description)

    @classmethod
    def prompt(cls, info):
        cls.console.clear()
        panel = Panel(info, width=100, title="[red]!Error!", style="red")
        cls.console.print(panel, "[cyan]> ...", justify="center")
        cls.getch()

    @staticmethod
    def back(inp):
        return inp.isdigit() and int(inp) == 0

    # @staticmethod
    # def skip(inp):
    #     return inp.isdigit() and int(inp) == 1


class LoginMenu:
    @classmethod
    def sign_up(cls):
        dic = {"Username": "", "Email": "", "Password": ""}
        ls = ["Sign Up", "Back"]

        while True:
            choice = Menu.choose("Sign Up", dic, ls)

            if choice in list(dic.keys()):
                inp = Menu.get_info(f"Input {choice}: ")
                if inp != "":
                    dic[choice] = inp

            elif choice == ls[0]:
                if "" in list(dic.values()):
                    Menu.prompt("Please Fill All The Fields")
                    
                elif UserController.exists(dic["Username"]):
                    Menu.prompt("Username Already Exists")
                    
                elif UserController.exists(dic["Email"]):
                    Menu.prompt("Email Already Exists")
                    
                elif not UserController.email_check(dic["Email"]):
                    Menu.prompt("Please Enter A Valid Email")
                    
                elif not UserController.password_check(dic["Password"]):
                    Menu.prompt("Password Must Be At Least 8 Characters")
                else:
                    break
            elif choice == ls[1]:
                return None

        user = User(dic["Username"], dic["Password"], dic["Email"], True)
        UserController.add_user(user)

        return user

    def check_user(data, password):
        if UserController.exists(data):
            if UserController.get_user(data).password == password:
                return True
        return False

    @classmethod
    def log_in(cls):
        dic = {"Username/Email": "", "Password": ""}
        ls = ["Login", "Back"]

        while True:
            choice = Menu.choose("Login", dic, ls)
            if choice in list(dic.keys()):
                inp = Menu.get_info(f"Input {choice}: ")
                if inp != "":
                    dic[choice] = inp

            elif choice == ls[0]:
                if "" in list(dic.values()):
                    Menu.prompt("Please Fill All The Fields")

                elif not cls.check_user(dic["Username/Email"], dic["Password"]):
                    Menu.prompt("Usrname Or Password Incorrect")
                else:
                    break

            elif choice == ls[1]:
                return None

        return UserController.get_user(dic["Username/Email"])

    @classmethod
    def get_user(cls):
        while True:
            options = ["Login", "Sign Up", "Exit"]
            choice = Menu.choose("login menu", options)
            if choice == options[0]:
                user = cls.log_in()
                if user == None:
                    continue
                return user

            elif choice == options[1]:
                user = cls.sign_up()
                if user == None:
                    continue
                return user

            elif choice == options[2]:
                return None


class TaskMenu:
    def __init__(self, user, project, task) -> None:
        self.__user = user
        self.__project = project
        self.__task: Task = task

    def edit_info(self):
        if self.__user.username not in self.__task.users:
            Menu.prompt("You Are Not Assigned To This Task")
            return

        dic = {
                "Name": self.__task.name,
                "State": self.__task.state.name,
                "Priority": self.__task.priority.name,
                "Starting Date": self.__task.starting_date,
                "Ending Date": self.__task.ending_date,
            }
        
        ls = ["Update Info","Back"]
        
        while True:
            choice = Menu.choose("New Task", dic, ls)
            if choice in list(dic.keys()):
                if choice == "State":
                    choice = Menu.choose(
                        "Choose The State",
                        [_state.name for _state in Task.State] + ["Back"],
                    )
                    if choice != "Back":
                        dic["State"] = choice
                elif choice == "Priority":
                    choice = Menu.choose(
                        "Choose The Priority",
                        [_priority.name for _priority in Task.Priority] + ["Back"],
                    )
                    if choice != "Back":
                        dic["Priority"] = choice
                else:
                    inp = Menu.get_info(f"Input {choice}: ")
                    if inp != "":
                        dic[choice] = inp
            elif choice == ls[0]:
                if dic["Name"] == "":
                    Menu.prompt("Please Input A Name")
                elif not Task.check_date(dic["Starting Date"]) or not Task.check_date(
                    dic["Starting Date"], dic["Ending Date"]
                ):
                    Menu.prompt("Please Input Valid Dates")
                else:
                    break
            else:
                return
        
        self.__task.name = (self.__user.username,dic["Name"])
        self.__task.starting_date = (self.__user.username,dic["Starting Date"])
        self.__task.ending_date = (self.__user.username,dic["Ending Date"])
        self.__task.state = (self.__user.username,Task.State[dic["State"]])
        self.__task.priority = (self.__user.username,Task.Priority[dic["Priority"]])
        
        ProjectController.update_project(self.__user.username,self.__project)
    
    def add_user(self):
        existing_users = [_user for _user in self.__project.users if _user not in self.__task.users]
        if not existing_users:
            Menu.prompt("No Users Available To Add")
            return
        
        while True:
            choice = Menu.choose("Add A New Assignee",existing_users+["Back"])
            
            if choice == "Back":
                break
            
            self.__task.add_user(self.__user.username,choice)
            existing_users.remove(choice)
            ProjectController.update_project(self.__user.username,self.__project)
    
    def remove_user(self):
        while True:
            choice = Menu.choose("Remove Users",self.__task.users+["Back"])
            
            if choice == "Back":
                break
            if choice == self.__project.leader:
                Menu.prompt("You Can't Remove The Leader")
                continue
            
            self.__task.remove_user(self.__user.username,choice)
            ProjectController.update_project(self.__user.username,self.__project)
    
        
    def manage_users(self):
        if self.__user.username != self.__project.leader:
            Menu.prompt("You Are Not The Leader Of This Project")
            return
        
        options = ["Add A New User","Remove A User","Back"]
        
        while True:
            choice = Menu.choose("Manage Users",options)
            
            if choice == options[0]:
                self.add_user()
            elif choice == options[1]:
                self.remove_user()
            else:
                break
        
    
    def comments(self):
        pass
    
    def history(self):
        pass
    
    
    def menu(self):
        options = ["Edit Info", "Manage Users", "Comments", "History", "Back"]

        while True:
            choice = Menu.choose(self.__task.name, options)

            if choice == options[0]:
                self.edit_info()
            elif choice == options[1]:
                self.manage_users()
            elif choice == options[2]:
                pass
            elif choice == options[3]:
                pass
            else:
                break


class ProjectMenu:
    def __init__(self, user, project) -> None:
        self.__user = user
        self.__project = project

    def tasks_table(self):
        if not self.__project.tasks:
            return None

        backlog = [
            Panel(f"name: {_task.name}\nid: {_task.id}", expand=True)
            for _task in self.__project.tasks
            if _task.state == Task.State.BackLog
        ]
        todo = [
            Panel(f"name: {_task.name}\nid: {_task.id}", expand=True)
            for _task in self.__project.tasks
            if _task.state == Task.State.ToDo
        ]
        doing = [
            Panel(f"name: {_task.name}\nid: {_task.id}", expand=True)
            for _task in self.__project.tasks
            if _task.state == Task.State.Doing
        ]
        done = [
            Panel(f"name: {_task.name}\nid: {_task.id}", expand=True)
            for _task in self.__project.tasks
            if _task.state == Task.State.Done
        ]
        archived = [
            Panel(f"name: {_task.name}\nid: {_task.id}", expand=True)
            for _task in self.__project.tasks
            if _task.state == Task.State.Archived
        ]

        tasks = [backlog, todo, doing, done, archived]

        table = Table(title="tasks")
        for state in Task.State:
            table.add_column(state.name, justify="center")

        max_tasks = max(len(_tasks) for _tasks in tasks)
        for i in range(max_tasks):
            row = []
            for task_list in tasks:
                if i < len(task_list):
                    row.append(task_list[i])
                else:
                    row.append("")
            table.add_row(*row)

        return table

    def choose_task(self) -> str:
        while True:
            table = self.tasks_table()
            Menu.console.clear()
            Menu.console.print(table,justify= "center")
            if table == None:
                Menu.prompt("No Tasks In This Project")
                return None

            inp = Menu.console.input("Input A Task ID(0 to go back): ")
            if Menu.back(inp):
                break
            elif not inp in [_task.id for _task in self.__project.tasks]:
                Menu.prompt("Please Enter A Valid ID")
            else:
                return inp

    def add_task(self):
        dic = {
            "Name": "",
            "State": Task.State.BackLog.name,
            "Priority": Task.Priority.Low.name,
            "Starting Date": Task.current_date(),
            "Ending Date": Task.default_ending_date(),
            "Description": "",
        }
        ls = ["Create Task", "Back"]

        while True:
            choice = Menu.choose("New Task", dic, ls)
            if choice in list(dic.keys()):
                if choice == "State":
                    choice = Menu.choose(
                        "Choose The State",
                        [_state.name for _state in Task.State] + ["Back"],
                    )
                    if choice != "Back":
                        dic["State"] = choice
                elif choice == "Priority":
                    choice = Menu.choose(
                        "Choose The Priority",
                        [_priority.name for _priority in Task.Priority] + ["Back"],
                    )
                    if choice != "Back":
                        dic["Priority"] = choice
                else:
                    inp = Menu.get_info(f"Input {choice}: ")
                    if inp != "":
                        dic[choice] = inp
            elif choice == ls[0]:
                if dic["Name"] == "":
                    Menu.prompt("Please Input A Name")
                elif not Task.check_date(dic["Starting Date"]) or not Task.check_date(
                    dic["Starting Date"], dic["Ending Date"]
                ):
                    Menu.prompt("Please Input Valid Dates")
                else:
                    break
            else:
                return

        id = Task.generate_id()
        task = Task(
            id,
            dic["Name"],
            dic["State"],
            dic["Priority"],
            dic["Starting Date"],
            dic["Ending Date"],
            dic["Description"],
            [self.__user.username],
        )

        self.__project.add_task(task)
        ProjectController.update_project(self.__user.username, self.__project)

    def remove_task(self):
        task_id = self.choose_task()
        print(task_id)
        Menu.getch()
        if task_id == None:
            return

        self.__project.remove_task(task_id)
        ProjectController.update_project(self.__user.username, self.__project)

    def manage_tasks(self):
        if self.__project.leader != self.__user.username:
            Menu.prompt("You Are Not The Leader Of This Project")
            return
        
        options = ["Add A New Task", "Remove A Task", "Back"]
        while True:
            choice = Menu.choose("Manage Tasks", options)
            if choice == options[0]:
                self.add_task()
            elif choice == options[1]:
                self.remove_task()
            elif choice == options[2]:
                break

    def remove_user(self):
        while True:
            choice = Menu.choose(
                "Choose A User To Remove", self.__project.users + ["Back"]
            )
            if choice != "Back":
                if self.__project.leader != choice:
                    self.__project.remove_user(choice)
                    ProjectController.update_project(
                        self.__user.username, self.__project
                    )
                else:
                    Menu.prompt("You Can't Remove The Leader")
            else:
                break

    def add_user(self):
        while True:
            inp = Menu.get_info("Input A Username/Email To Add (0 to go back): ")
            if Menu.back(inp):
                break
            elif not UserController.exists(inp):
                Menu.prompt("User Not Found")
            else:
                if inp in self.__project.users:
                    Menu.prompt("User Already In The Project")
                else:
                    self.__project.add_user(inp)
                    ProjectController.update_project(
                        self.__user.username, self.__project
                    )
                    break

    def manage_users(self):
        options = ["Add User", "Remove User", "Back"]

        while True:
            choice = Menu.choose("Manage Users", options)

            if choice == options[0]:
                self.add_user()
            elif choice == options[1]:
                self.remove_user()
            else:
                break

    def menu(self):
        ls = ["Open A Task", "Manage Tasks", "Manage Members", "Back"]
        while True:
            choice = Menu.choose(self.__project.name, ls)
            if choice == ls[0]:
                task_id = self.choose_task()
                if task_id != None:
                    task = self.__project.get_task(task_id)
                    task_menu = TaskMenu(self.__user,self.__project,task)
                    task_menu.menu()
            elif choice == ls[1]:
                self.manage_tasks()
            elif choice == ls[2]:
                self.manage_users()
            elif choice == ls[3]:
                break


class UserMenu:
    def __init__(self, user) -> None:
        self.__user = user

    def craete_projects_table(self):
        projects = ProjectController.get_projects(self.__user.username)
        if not projects:
            return None

        table = Table(title="Projects")
        table.add_column("name")
        table.add_column("id")
        table.add_column("leader")
        for project in projects:
            table.add_row(project.name, project.id, project.leader)

        return table

    def get_project(self):
        while True:

            table = self.craete_projects_table()
            if table == None:
                Menu.prompt("No Projects Available")
                return
            Menu.console.clear()
            Menu.console.print(table, justify="center")
            id = Menu.console.input("Input An ID (0 to go back): ")
            if Menu.back(id):
                return None
            elif not ProjectController.exists(id, self.__user.username):
                Menu.prompt("Enter A Valid ID")
            else:
                break

        return ProjectController.get_project(self.__user.username, id)

    def create_new_project(self):
        dic = {"ID": "", "Name": ""}
        ls = ["Create", "Back"]

        while True:
            choice = Menu.choose("New Project", dic, ls)

            if choice in list(dic.keys()):
                inp = Menu.get_info(f"Input {choice}: ")
                if inp != "":
                    dic[choice] = inp
            elif choice == ls[0]:
                if "" in list(dic.values()):
                    Menu.prompt("Please Fill All The Fields")
                elif ProjectController.exists(dic["ID"]):
                    Menu.prompt("ID Already Exists")
                elif len(dic["ID"]) < 3:
                    Menu.prompt("ID Must Be At Least 3 Characters")
                else:
                    project = Project(
                        dic["Name"],
                        [],
                        [self.__user.username],
                        self.__user.username,
                        dic["ID"],
                    )
                    ProjectController.add_project(self.__user.username, project)
                    break
            else:
                break

    def remove_project(self):
        project: Project
        while True:
            project = self.get_project()
            if project == None:
                return
            if project.leader != self.__user.username:
                Menu.prompt("You Are Not This Project's Leader")
            else:
                break

        ProjectController.remove_project(self.__user.username, project)

    def manage_projects(self):
        while True:
            options = ["Create A New Project", "Remove A Project", "Back"]
            choice = Menu.choose("Manage Projects", options)
            if choice == options[0]:
                self.create_new_project()
            elif choice == options[1]:
                self.remove_project()
            else:
                break

    def Projects(self):
        options = ["Open A Project", "Manage Projects", "Back"]

        while True:
            choice = Menu.choose("Projetcs", options)
            if choice == options[0]:
                project = self.get_project()
                if project != None:
                    project_menu = ProjectMenu(self.__user, project)
                    project_menu.menu()
            elif choice == options[1]:
                self.manage_projects()
            elif choice == options[2]:
                break

    def edit_info(self):
        dic = {
            "Username": self.__user.username,
            "Email": self.__user.email,
            "Password": self.__user.password,
        }

        ls = ["Confirm", "Back"]

        while True:
            choice = Menu.choose("Edit Info", dic, ls)
            if choice in list(dic.keys()):
                if choice == "Username":
                    Menu.prompt("Can't Change Your Username")
                    continue

                inp = Menu.get_info(f"Input a new {choice}: ")
                if inp != "":
                    dic[choice] = inp

            elif choice == ls[0]:
                if UserController.exists(dic["Email"]):
                    Menu.prompt("Email Already Exists")

                elif not UserController.email_check(dic["Email"]):
                    Menu.prompt("Please Eneter A Valid Email")

                elif not UserController.password_check(dic["Password"]):
                    Menu.prompt("Password Must Be At Least 8 characters")
                else:
                    break
            else:
                return

        self.__user.email = dic["Email"]
        self.__user.password = dic["Password"]
        UserController.upadate_user(self.__user)

    def menu(self):
        ls = ["Projects", "Edit Your Profile", "Sign Out"]
        while True:
            choice = Menu.choose(f"{self.__user.username}", ls)

            if choice == ls[0]:
                self.Projects()
            elif choice == ls[1]:
                self.edit_info()
            elif choice == ls[2]:
                break

