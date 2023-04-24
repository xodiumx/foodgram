from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User

MIN_OF_AMOUNT = 1
MAX_OF_AMOUNT = 5000
MIN_OF_COOKING_TIME = 1
MAX_OF_COOKING_TIME = 500
MAX_LENGTH_OF_DESCRIPTION = 2000
LENGTH_OF_RECIPE_NAME = 120
LENGTH_OF_INGREDIENT_NAME = 120


class Tag(models.Model):
    """
    Модель тэгов:
    Attributes:
        - name: Название
        - color: Цвет в формате hex
        - slug: Уникальный слаг
    """
    name = models.CharField(
        'Тэг',
        max_length=50,
        null=False,
        blank=False,
    )
    color = models.CharField(
        'Цвет',
        max_length=16,
        null=False,
        blank=False,)
    slug = models.SlugField(
        max_length=16,
        unique=True,
        null=False,
        blank=False,)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """
    Модель ингредиентов:
    Attributes:
        - name: Название
        - amount: Количество
        - measurement_unit: Ед. измерения
    """
    name = models.CharField(
        'Ингредиент',
        max_length=LENGTH_OF_INGREDIENT_NAME,
        db_index=True,
        null=False,
        blank=False)
    measurement_unit = models.CharField(
        'Ед. измерения',
        max_length=20,
        null=False,
        blank=False,)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """
    Модель для рецептов.
    Attributes:
        - author: Автор рецепта
        - name: Название
        - image: Картинка
        - description: Описание
        - ingredients: Ингрединты
        - tags: Тэги
        - cooking_time: Время приготовления
    """
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
        null=False,
        blank=False
    )
    name = models.CharField(
        'Название рецепта',
        max_length=LENGTH_OF_RECIPE_NAME,
        db_index=True,
        null=False,
        blank=False
    )
    image = models.ImageField(
        'Картинка',
        upload_to='recipes/',
        null=False,
        blank=False
    )
    text = models.TextField(
        'Описание',
        max_length=MAX_LENGTH_OF_DESCRIPTION,
        null=False,
        blank=False
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        blank=True,
        related_name='recipes',
        verbose_name='Ингредиенты',
        through='AmountIngredient',)
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='recipes',
        verbose_name='Тэги',
        through='RecipeTag',)
    cooking_time = models.IntegerField(
        'Время приготовления',
        validators=(
            MaxValueValidator(
                MAX_OF_COOKING_TIME,
                message=f'Максимальное количесвто {MAX_OF_COOKING_TIME} мин.'),
            MinValueValidator(
                MIN_OF_COOKING_TIME,
                message=f'Минимальное количесвто {MIN_OF_COOKING_TIME} минута')
        ),
        null=False,
        blank=False
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class AmountIngredient(models.Model):
    """
    Модель для связи количества ингредиентов.
    Attributes:
        - ingredient: FK to Ingredient model
        - recipe: FK to Recipe model
        - amount: integer value
    """
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    amount = models.IntegerField(
        'Количество',
        default=1,
        validators=(
            MinValueValidator(
                MIN_OF_AMOUNT,
                message=f'Минимальное количесвто {MIN_OF_AMOUNT}'),
            MaxValueValidator(
                MAX_OF_AMOUNT,
                message=f'Максимальное количество {MAX_OF_AMOUNT}')
        )
    )

    class Meta:
        verbose_name = 'Количество ингредента'
        verbose_name_plural = 'Количество ингредентов'
        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'ingredient'),
                name='unique_recipe_ingredient',
                violation_error_message='Повторное добавление ингредиента',
            )
        ]


class RecipeTag(models.Model):
    """
    Модель для связи рецептов и тегов.
    Attributes:
        - tag: FK to Tag model
        - recipe: FK to Recipe model
    """
    tag = models.ForeignKey(Tag, on_delete=models.PROTECT)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Теги рецепта'
        verbose_name_plural = 'Теги рецептов'


class Favorite(models.Model):
    """
    Модель для добавления рецептов в избранное.
    Attributes:
        - user: FK to User model
        - recipe: FK to Recipe model
    """
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'user'),
                name='unique_recipe_user_favorite',
                violation_error_message='Повторная подписка',
            )
        ]
    

class ShoppingCart(models.Model):
    """
    Модель для добавления рецептов в корзину.
    Attributes:
        - user: FK to User model
        - recipe: FK to Recipe model
    """
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-id',)
        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'user'),
                name='unique_recipe_user_cart',
                violation_error_message='Повторное добавление в корзину',
            )
        ]
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
