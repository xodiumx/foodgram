# Generated by Django 4.1.8 on 2023-04-19 11:50

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AmountIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(500), django.core.validators.MinValueValidator(1)], verbose_name='Количество')),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=120, verbose_name='Ингредиент')),
                ('measurement_unit', models.CharField(max_length=20, verbose_name='Ед. измерения')),
            ],
            options={
                'verbose_name': 'Ингредиент',
                'verbose_name_plural': 'Ингредиенты',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=120, verbose_name='Название рецепта')),
                ('image', models.ImageField(upload_to='recipes/', verbose_name='Картинка')),
                ('text', models.TextField(max_length=500, verbose_name='Описание')),
                ('cooking_time', models.IntegerField(validators=[django.core.validators.MaxValueValidator(500), django.core.validators.MinValueValidator(1)], verbose_name='Время приготовления')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('ingredients', models.ManyToManyField(blank=True, related_name='recipes', through='recipes.AmountIngredient', to='recipes.ingredient', verbose_name='Ингредиенты')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Тэг')),
                ('color', models.CharField(max_length=16, verbose_name='Цвет')),
                ('slug', models.SlugField(max_length=16, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='RecipeTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='recipes.tag')),
            ],
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='recipes', through='recipes.RecipeTag', to='recipes.tag', verbose_name='Тэги'),
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
        migrations.AddField(
            model_name='amountingredient',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='recipes.ingredient'),
        ),
        migrations.AddField(
            model_name='amountingredient',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe'),
        ),
        migrations.AddConstraint(
            model_name='shoppingcart',
            constraint=models.UniqueConstraint(fields=('recipe', 'user'), name='unique_recipe_user_cart', violation_error_message='Повторная добавление в корзину'),
        ),
        migrations.AddConstraint(
            model_name='favorite',
            constraint=models.UniqueConstraint(fields=('recipe', 'user'), name='unique_recipe_user_favorite', violation_error_message='Повторная подписка'),
        ),
    ]
