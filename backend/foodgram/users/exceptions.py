from rest_framework.exceptions import ValidationError


class WrongData(ValidationError):
    ...


class CantSubscribe(ValidationError):
    ...