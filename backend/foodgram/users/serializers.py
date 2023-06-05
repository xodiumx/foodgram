from collections import OrderedDict

from recipes.models import Recipe
from rest_framework.serializers import (CharField, EmailField, ListSerializer,
                                        ModelSerializer, Serializer,
                                        SerializerMethodField)

from .models import Follow, User
from .services import UserService


class InfoSerializer(ModelSerializer):
    """Сериализация информации о пользователе."""
    is_subscribed = SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', )

    def get_is_subscribed(self, obj: Follow) -> bool:
        request = self.context.get('request')
        return UserService.is_subscribed(self, obj, request)


class SignupSerializer(ModelSerializer):
    """Сериализациия данных регистрации пользователя."""
    class Meta:
        model = User
        fields = ('email', 'id', 'password', 'username', 'first_name',
                  'last_name',)

    def validate(self, data: OrderedDict) -> OrderedDict:
        return UserService.validate_signup(self, data)

    def create(self, validated_data: dict) -> User:
        return UserService.create_user(self, validated_data)

    def to_representation(self, instance: User) -> OrderedDict:
        """Убрать пароль из ответа."""
        data = super().to_representation(instance)
        data.pop('password')
        return data


class LoginSerializer(Serializer):
    """
    Сериализация данных при авторизации пользователя.
    При успешной авторизации выдаем token и записываем последнее посещение.
    """
    email = EmailField(max_length=254)
    password = CharField(max_length=64)

    def validate(self, data: OrderedDict) -> dict:
        return UserService.validate_login(self, data)


class ChangePasswordSerializer(Serializer):
    """
    Сериализция данных изменения пароля.
    Если старый пароль введен верно записываем новый захешированный пароль.
    """
    new_password = CharField(max_length=64)
    current_password = CharField(max_length=64)

    def validate(self, data: OrderedDict) -> OrderedDict:
        return UserService.validate_password(self, data)


class RecipeInfoSerializer(ModelSerializer):
    """Информация о рецепте, для подписки на пользователя."""
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubInfoSerializer(ModelSerializer):
    """Сериализация данных при подписке на пользователя."""
    recipes = RecipeInfoSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'recipes')

    def to_representation(self, instance: User) -> OrderedDict:
        """
        Добавляем поля is_subscribed, recipes_count в запрос и ограничиваем
        вывод рецептов исходя из переданного лимита.
        """
        data = super().to_representation(instance)
        request = self.context.get('request')

        limit = request.query_params.get('recipes_limit')
        if limit:
            data['recipes'] = data['recipes'][:int(limit)]

        user = request.user
        data['is_subscribed'] = Follow.objects.filter(
            user=user, following=instance).exists()
        data['recipes_count'] = len(data['recipes'])
        return data


class SubscriptionSerializer(ListSerializer):
    """Сериализация всех подписок пользователя."""
    child = SubInfoSerializer()
