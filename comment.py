class Comment:
    def __init__(self , text : str , date : str, user : str, id: int) -> None:
        self.__text = text
        self.__date = date
        self.__user = user
        self.__id = id

    @property
    def text(self) -> str:
        return self.__text

    @property
    def date(self) -> str:
        return self.__date

    @property
    def user(self) -> str:
        return self.__user

    @property
    def id(self) -> int:
        return self.__id
