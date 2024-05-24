from user import UserController, User, ProjectController, Project, Task


class Menu:
    @staticmethod
    def Choose(options):
        while True:
            for i in range(len(options)):
                print(i + 1, options[i], sep=". ")

            choice = input("Choose An Option: ")
            if not choice.isdigit():
                break

            choice = int(choice)
            if 1 <= choice <= len(options):
                return choice

    @staticmethod
    def back(inp):
        return inp.isdigit() and int(inp) == 0

    @staticmethod
    def skip(inp):
        return inp.isdigit() and int(inp) == 1


class LoginMenu:
    @staticmethod
    def input_username():
        while True:
            username = input("username  (0 to go back): ")
            if Menu.back(username):
                return None
            if not UserController.exists(username):
                return username

            print("username already exists")

    @staticmethod
    def input_email():
        while True:
            email = input("email  (0 to go back): ")
            if Menu.back(email):
                return None
            if not UserController.email_check(email):
                print("please input a correct email")
                continue
            if UserController.exists(email):
                print("email already exists")
                continue

            return email

    @staticmethod
    def input_password():
        while True:
            password = input("password  (0 to go back): ")
            if Menu.back(password):
                return None
            if UserController.password_check(password):
                return password

            print("password must be atleast 8 characters")

    @staticmethod
    def sign_up():
        username: str
        email: str
        password: str
        while True:
            username = LoginMenu.input_username()
            if username == None:
                return None
            if UserController.exists(username):
                print("username already exists")
                continue

            break

        while True:
            email = LoginMenu.input_email()
            if email == None:
                return None
            if UserController.exists(email):
                print("email already exists")
                continue
            break

        while True:
            password = LoginMenu.input_password()
            if password == None:
                return None

            break

        user = User(username, password, email, True, [])
        UserController.add_user(user)
        return user

    @staticmethod
    def log_in():
        while True:
            info = input("email or username(0 to go back): ")
            if Menu.back(info):
                return None

            if not UserController.exists(info):
                print("user not found")
                continue

            password = input("password(0 to go back): ")
            if Menu.back(password):
                return None

            user = UserController.get_user(info)
            if not user.enabled:
                print("user not found")
                continue
            if user.password != password:
                print("wrong password")
                continue

            return user

    @staticmethod
    def get_user():
        while True:
            options = ["Login", "Sign Up", "Exit"]
            choice = Menu.Choose(options)
            if choice == 1:
                while True:
                    user = LoginMenu.log_in()
                    if user == None:
                        break
                    return user

            elif choice == 2:
                while True:
                    user = LoginMenu.sign_up()
                    if user == None:
                        break
                    return user

            elif choice == 3:
                break


class TaskMenu:
    def __init__(self, user: User, project: Project, task: Task) -> None:
        self.__task : Task = task
        self.__project = project
        self.__user = user

    def show_info(self):
        print(*self.__task.get_dict(), sep="\n----\n")
    
    def edit_info(self):
        if self.__user.username not in self.__task.users:
            print("you are not assigned to this task")
            return

        while True:
            options = [
                "change name",
                "change priority",
                "chnage state",
                "change ending date",
                "change the description",
                "back",
            ]
            ProjectController.update_project(self.__user.username, self.__project)
            choice = Menu.Choose(options)
            if choice == 1:
                name = input("choose a new name(0 to go back)")
                if Menu.back(name):
                    continue
                self.__task.name = (self.__user.username,name)

            elif choice == 2:
                options = [_priority.name for _priority in Task.Priority] + ["back"]
                choice = Menu.Choose(options)
                print(choice)
                if choice == len(options):
                    continue

                self.__task.priority = Task.Priority[options[choice - 1]]

            elif choice == 3:
                options = [_state.name for _state in Task.State] + ["back"]
                choice = Menu.Choose(options)
                if choice == len(options):
                    continue

                self.__task.state = Task.State[options[choice - 1]]

            elif choice == 4:
                date: str
                while True:
                    date = input("enter a valid date YYYY-MM-DD (0 to go back): ")
                    if Menu.back(date):
                        break

                    if Task.check_date(self.__task.starting_date, date):
                        self.__task.ending_date = date
                        break

                    print("date not valid")
                
            elif choice == 5:
                description = input("new description(0 to go back): ")
                self.__task.description = description
                
            elif choice == 6:
                break
        
    def add_user(self):
        # all_users = [_user for _user in self.__project.users]
        # task_users = [_user.username for _user in self.__task.users]
        remaining_users = [_user for _user in self.__project.users if _user not in self.__task.users]
    
        options = remaining_users + ["back"]
        choice = Menu.Choose(options)
        
        if choice != len(options):
            self.__task.add_user(remaining_users[choice-1])
        
        ProjectController.update_project(self.__user.username,self.__project)
        
    def remove_user(self):
        options = self.__task.users + ["back"]
        choice = Menu.Choose(options)
        
        if choice != len(options):
            removed_user = options[choice-1]
            
            if removed_user != self.__project.leader:
                self.__task.remove_user(options[choice-1])
            else:
                print("you can't remove the leader")  
        
        ProjectController.update_project(self.__user.username,self.__project)
        
    def user_manager(self):
        print(self.__user.username)
        print(self.__project.leader)
        if self.__user.username != self.__project.leader:
            print("you are not the leader")
            return
        
        options = ["add user","remove user","back"]
        
        while True:
            choice = Menu.Choose(options)
            if choice == 1:
                self.add_user()
            elif choice == 2:
                self.remove_user()
            else:
                break

    def menu(self):
        options = ["edit info", "manage users", "comments", "history", "back"]
        while True:
            # self.show_info()
            choice = Menu.Choose(options)
            if choice == 1:
                self.edit_info()
            elif choice == 2:
                self.user_manager()
            elif choice == 3:
                pass #comments
            elif choice == 4:
                pass #history
            elif choice == 5:
                break


class ProjectMenu:
    def __init__(self, user: User, project: Project) -> None:
        self.__user = user
        self.__project = project

    def showtasks(self):
        tasks = self.__project.tasks
        print(*[(task.name, task.id) for task in tasks], sep="---------")

    def change_name(self):
        while True:
            new_name = input("new name(0 to go back): ")
            if Menu.back(new_name):
                break
            if new_name == self.__project.name:
                print("names must be diffrent")
                continue

            self.__project.name = new_name
            ProjectController.update_project(self.__user.username, self.__project)
            break

    def add_user(self):
        while True:
            username = input("input username(0 to go back): ")
            if not Menu.back(username):
                if UserController.exists(username):
                    if username not in self.__project.users:
                        self.__project.add_user(username)
                        print("user:", self.__user)
                        ProjectController.update_project(
                            self.__user.username, self.__project
                        )
                        break
                    else:
                        print("already in the project")
                else:
                    print("username doesn't exist")
            else:
                break

    def remove_user(self):
        options = [*self.__project.users] + ["back"]
        size = len(options)

        while True:
            choice = Menu.Choose(options) - 1

            if choice == size - 1:
                break

            chosen_user = options[choice]
            if self.__project.leader != chosen_user:
                self.__project.remove_user(chosen_user)
                ProjectController.update_project(self.__user.username, self.__project)
                break

            print("you can't remove the leader")

    def manage_users(self):
        while True:
            options = ["add user", "remove user", "back"]
            choice = Menu.Choose(options)
            if choice == 1:
                self.add_user()
            elif choice == 2:
                self.remove_user()
            elif choice == 3:
                break

    def change_info(self):
        options = ["change name", "manage users", "back"]
        while True:
            choice = Menu.Choose(options)
            if choice == 1:
                self.change_name()
            elif choice == 2:
                self.manage_users()
            elif choice == 3:
                break

    def choose_task(self):
        options = [(_task.name, _task.id) for _task in self.__project.tasks] + ["back"]
        if len(options) == 1:
            print("no tasks available")
            return None
        choice = Menu.Choose(options)
        if choice == len(options):
            return None

        return self.__project.tasks[choice - 1]

    def add_task(self):
        id = Task.generate_id()

        name = input("enter a name(0 to go back): ")
        if Menu.back(name):
            return

        starting_date: str
        while True:
            starting_date = input(
                "enter a starting date in (Y-M-D) form (0 to go back,1 to skip): "
            )
            if Menu.back(starting_date):
                return

            if Menu.skip(starting_date):
                starting_date = Task.current_date()
                break
            else:
                if Task.check_date(starting_date):
                    break

            print("please enter a valid date")

        ending_date: str
        while True:
            ending_date = input(
                "enter an edning date in (Y-M-D) form (0 to go back,1 to skip): "
            )
            if Menu.back(starting_date):
                return

            if Menu.skip(ending_date):
                ending_date = Task.default_ending_date()
                break

            else:
                if Task.check_date(starting_date, ending_date):
                    break

            print("please enter a valid date")

        state: str
        options = [_state.name for _state in Task.State] + ["skip", "back"]
        choice = Menu.Choose(options)

        if choice == len(options):
            return

        if choice == len(options) - 1:
            state = Task.State.BackLog.name
        else:
            state = Task.State[options[choice - 1]].name

        priority: str
        options = [_priority.name for _priority in Task.Priority] + ["skip", "back"]
        choice = Menu.Choose(options)
        if choice == len(options):
            return

        if choice == len(options) - 1:
            priority = Task.Priority.Low.name
        else:
            priority = Task.Priority[options[choice - 1]].name

        description = input("put some description(0 to go back and 1 to skip): ")
        if Menu.back(description):
            return
        elif Menu.skip(description):
            description = ""

        users = [self.__project.leader]

        task = Task(
            id, name, state, priority, starting_date, ending_date, description, users
        )
        self.__project.add_task(task)
        ProjectController.update_project(self.__user.username, self.__project)

    def remove_task(self):
        task = self.choose_task()
        if task == None:
            return
        self.__project.remove_task(task)
        ProjectController.update_project(self.__user.username, self.__project)

    def task_manager(self):
        options = ["open a task", "create a new task", "remove a task", "back"]
        while True:
            choice = Menu.Choose(options)

            if choice == 1:
                task = self.choose_task()
                if task != None:
                    task_menu = TaskMenu(self.__user, self.__project, task)
                    task_menu.menu()
            elif choice == 2:
                self.add_task()
            elif choice == 3:
                print("you chose remove")
                self.remove_task()
            elif choice == 4:
                break

    def menu(self):
        options = ["tasks", "change project info", "back"]
        while True:
            self.showtasks()
            print("\n")
            choice = Menu.Choose(options)
            if choice == 1:
                self.task_manager()
            elif choice == 2:
                self.change_info()
            elif choice == 3:
                break


class UserMenu:
    def __init__(self, user) -> None:
        self.__user = user

    @property
    def user(self):
        return self.__user

    @user.setter
    def user(self, user: User):
        self.user = user

    def PreviousProjects(self):
        while True:
            projects = ProjectController.get_projects(self.__user.username)
            project_names = [_project.name for _project in projects]
            project_names.append("back")
            size = len(project_names)
            choice = Menu.Choose(project_names) - 1

            print(choice)
            if choice == size - 1:
                break
            project_menu = ProjectMenu(self.__user, projects[choice])
            project_menu.menu()

    def CreateNewProject(self):
        pass

    def Projects(self):
        options = ["Previous Projects", "Create A New Project", "Back"]

        while True:
            choice = Menu.Choose(options)

            if choice == 1:
                self.PreviousProjects()

            elif choice == 2:
                pass
            elif choice == 3:
                break

    def menu(self):
        options = ["projects", "change profile", "exit"]
        while True:
            choice = Menu.Choose(options)

            if choice == 1:
                project = self.Projects()
                print(project.name)
            elif choice == 2:
                pass
            elif choice == 3:
                pass
