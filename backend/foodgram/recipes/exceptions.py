from rest_framework.exceptions import ValidationError


class CantSubscribe(ValidationError):
    ...