from user import User

class Comment:
    def __init__(self , id : int , text : str , user : User) -> None:
        self.__id = id
        self.__text = text
        self.__user = user

    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, new_id: int) -> None:
        self.__id = new_id

    @property
    def text(self) -> str:
        return self.__text

    @text.setter
    def text(self, new_text: str) -> None:
        self.__text = new_text

    @property
    def user(self) -> User:
        return self.__user

    @user.setter
    def user(self, new_user: User) -> None:
        self.__user = new_user
