class DataBaseError(Exception):

    def __init__(self, name: str) -> None:
        self.name = name
        super().__init__(self.name)

    def __str__(self) -> str:
        return f"Ошибка в методе {self.name} класса CRUD"


class JWTCreateError(Exception):
    def __init__(self, name: str) -> None:
        self.name = name
        super().__init__(self.name)

    def __str__(self) -> str:
        return f"Ошибка в методе {self.name} класса JWTCreate"


class SendError(Exception):

    def __init__(self, name: str) -> None:
        self.name = name
        super().__init__(self.name)

    def __str__(self) -> str:
        return f"Ошибка в методе {self.name} класса Send. Пришли неверные данные"


class PasswordError(Exception):
    def __init__(self, name: str) -> None:
        self.name = name
        super().__init__(self.name)

    def __str__(self) -> str:
        return f"Ошибка в методе {self.name}. Неверный пароль"
