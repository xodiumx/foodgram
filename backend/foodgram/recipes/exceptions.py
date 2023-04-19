from rest_framework.exceptions import ValidationError


class CantSubscribe(ValidationError):
    ...


class NotUniqueIngredient(ValidationError):
    ...


class NotUniqueTag(ValidationError):
    ...
