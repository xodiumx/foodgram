from rest_framework.exceptions import ValidationError


class UserIsNotAuth(ValidationError):
    """400 ошибка для не аутентифицированного пользователя."""
    ...


class CantAddTwice(ValidationError):
    """
    400 ошибка - нельзя повторно добавлять ингредиент в избранное и корзину.
    """
    ...


class IngredientError(ValidationError):
    """
    400 ошибка - ингредиент уже добавлен в рецепт или не валидно количество.
    """
    ...
