class User:
    def __init__(self,username,password,email,enabled,projects) -> None:
        self.username = username
        self.password = password
        self.email = email
        self.enabled = enabled
        self.projects = projects if projects else []
    
    @property
    def getUsername(self):
        return self.username
    
    @getUsername.setter
    def setUsername(self,newUsername):
        self.username = newUsername

    @property
    def getPassword(self):
        return self.password
    
    @getPassword.setter
    def setPassword(self,newPassword):
        self.password = newPassword

    @property
    def getEmail(self):
        return self.email
    
    @getEmail.setter
    def setEmail(self,newEmail):
        self.email = newEmail

    @property
    def getEnabled(self):
        return self.enabled
    
    @getEnabled.setter
    def setEnabled(self,newEnabled):
        self.enabled = newEnabled
    
    @property
    def getProjects(self):
        return self.projects

    def addProject(self,newProject):
        if newProject.id not in self.projects.id :
            self.projects.append(newProject)
    
    def removeProject(self,delproject):
        if delproject.id in self.projects.id:
            self.projects.remove(delproject)
        else :
            return False
