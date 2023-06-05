from collections import OrderedDict

from recipes.models import (MAX_OF_AMOUNT, MIN_OF_AMOUNT, AmountIngredient,
                            Favorite, Recipe, ShoppingCart)

from .exceptions import IngredientError


class RecipeSerivce:

    def validate_recipe(self, data: OrderedDict) -> OrderedDict:
        """
        В data записываем ingredient-ы так как они сериализуются
        только для чтения.
        """
        ingredients = self.initial_data.get('ingredients')
        ingredient_ids = [ingredient.get('id') for ingredient in ingredients]

        if len(ingredient_ids) != len(set(ingredient_ids)):
            raise IngredientError({'ingredient': 'Ингредиент уже добавлен'})
        
        amounts = [ing.get('amount') for ing in ingredients
                   if MIN_OF_AMOUNT <= int(ing.get('amount')) <= MAX_OF_AMOUNT]
        
        if len(amounts) != len(ingredients):
            raise IngredientError(
                {'amount': 'количество должно быть '
                 f'больше {MIN_OF_AMOUNT} и меньше {MAX_OF_AMOUNT}'})
        data['ingredients'] = ingredients
        return data
    
    def create_recipe(self, validated_data: dict) -> Recipe:
        """
        При создании рецепта:
        - Извлекаем из validated_data теги и ингредиенты
        - Создаем запись в модели Recipe
        - Добавляем к объекту recipe теги
        - Создаем в связанной таблице AmountIngredient записи об ингредиентах и
          их количестве.
        """
        tags = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)

        AmountIngredient.objects.bulk_create(
            [AmountIngredient(
                recipe=recipe,
                ingredient_id=ingredient_data.pop('id'),
                amount=ingredient_data.pop('amount')
            ) for ingredient_data in ingredients_data])
        return recipe
    
    def update_recipe(self, instance: Recipe, validated_data: dict) -> Recipe:
        """
        Если есть запись обновления поля, берем ее из validated_data иначе
        берем уже имеющуюся запись.
        Информацию об ингредиентах отчищаем и создаем по новой.
        """
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get(
            'text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )

        instance.tags.clear()
        instance.tags.set(validated_data.get('tags'))

        AmountIngredient.objects.filter(recipe=instance).all().delete()
        AmountIngredient.objects.bulk_create(
            [AmountIngredient(
                recipe=instance,
                ingredient_id=ingredient_data.pop('id'),
                amount=ingredient_data.pop('amount')
            ) for ingredient_data in validated_data.get('ingredients')])
        instance.save()
        return instance

    def get_favorite(self, obj: Recipe) -> Favorite:
        return Favorite.objects.filter(
            user_id=self.context.get('request').user.id,
            recipe=obj).exists()

    def get_shopping_cart(self, obj: Recipe) -> ShoppingCart:
        return ShoppingCart.objects.filter(
            user_id=self.context.get('request').user.id,
            recipe=obj).exists()
