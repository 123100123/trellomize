class User:
    def __init__(self,username,password,email,enabled) -> None:
        self.username = username
        self.password = password
        self.email = email
        self.enabled = enabled