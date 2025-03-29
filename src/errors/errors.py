class DataBaseError(Exception):

    def __init__(self, detail: str) -> None:
        self.detail = detail
        super().__init__(self.detail)

    def __str__(self) -> str:
        return self.detail


class JWTCreateError(Exception):
    def __init__(self, detail: str) -> None:
        self.detail = detail
        super().__init__(self.detail)

    def __str__(self) -> str:
        return self.detail


class SendError(Exception):

    def __init__(self, detail: str) -> None:
        self.detail = detail
        super().__init__(self.detail)

    def __str__(self) -> str:
        return self.detail


class PasswordError(Exception):
    def __init__(self, detail: str) -> None:
        self.detail = detail
        super().__init__(self.detail)

    def __str__(self) -> str:
        return self.detail


class EmailError(Exception):
    def __init__(self, detail: str) -> None:
        self.detail = detail
        super().__init__(self.detail)

    def __str__(self) -> str:
        return self.detail


class PhoneNumberError(Exception):
    def __init__(self, detail: str) -> None:
        self.detail = detail
        super().__init__(self.detail)

    def __str__(self) -> str:
        return self.detail
