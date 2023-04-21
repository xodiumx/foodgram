from rest_framework.exceptions import AuthenticationFailed, ValidationError


class WrongData(ValidationError):
    """400 ошибка при не корректных данных."""
    ...


class CantSubscribe(ValidationError):
    """400 ошибка при повторной подписке и подписке на себя."""
    ...


class UserIsNotAuthenticated(AuthenticationFailed):
    """401 ошибка если пользователь не авторизован."""
    ...
