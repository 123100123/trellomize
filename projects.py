class Project:
    def __init__(self,name,id,tasks,users,leader) :
        self.name = name
        self.id = id
        self.leader = leader
        self.tasks = tasks if tasks else []
        self.users = users if users else []
    
    @property
    def getName(self):
        return self.name
    
    @getName.setter
    def setName(self,newName):
        self.name = newName

    @property
    def getLeader(self):
        return self.leader
    
    @property
    def getId(self):
        return self.id
    
    @property
    def getUsers(self):
        return self.users
    
    def addUser(self,newUser):
        if newUser.username not in self.users.username :
            self.users.append(newUser)
    
    def removeUser(self,delUser):
        if delUser.username in self.users.username:
            self.users.remove(delUser)
        else :
            return False