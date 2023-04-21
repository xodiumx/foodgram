from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.serializers import (CharField, EmailField, ListSerializer,
                                        ModelSerializer, Serializer,
                                        SerializerMethodField)

from recipes.models import Recipe

from .exceptions import WrongData
from .models import Follow, User
from .utils import get_tokens_for_user


class InfoSerializer(ModelSerializer):
    """Сериализация информации о пользователе."""
    is_subscribed = SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', )

    def get_is_subscribed(self, follow):
        request = self.context.get('request')
        return Follow.objects.filter(
            user=None if request.user.is_anonymous else request.user,
            following=follow).exists()


class SignupSerializer(ModelSerializer):
    """Сериализациия данных регистрации пользователя."""
    class Meta:
        model = User
        fields = ('email', 'id', 'password', 'username', 'first_name',
                  'last_name',)

    def create(self, validated_data):
        """Хешируем пароль через set_password."""
        user = User.objects.create(**validated_data)
        user.set_password(user.password)
        user.save()
        return user

    def to_representation(self, instance):
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

    def validate(self, data):
        user = get_object_or_404(User, email=data.get('email'))
        if not check_password(data.get('password'), user.password):
            raise WrongData('Введены не правильные данные')
        user.last_login = timezone.now()
        user.save()
        return {'auth_token': get_tokens_for_user(user).get('access')}


class ChangePasswordSerializer(Serializer):
    """
    Сериализция данных изменения пароля.
    Если старый пароль введен верно записываем новый захешированный пароль.
    """
    new_password = CharField(max_length=64)
    current_password = CharField(max_length=64)

    def validate(self, data):
        user = get_object_or_404(User, username=self._args[0])
        if not check_password(data.get('current_password'), user.password):
            raise WrongData('Введен не правильный пароль')
        user.set_password(data.get('new_password'))
        user.save()
        return data


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

    def to_representation(self, instance):
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
