from collections import OrderedDict

from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.request import Request

from .exceptions import WrongData
from .models import Follow, User
from .utils import get_tokens_for_user


class UserService:
    
    def validate_signup(self, data: OrderedDict) -> OrderedDict:
        """
        - Если username - 'me' рейзим ошибку
        - приводим username и email к lowercase
        """
        if data.get('username') == 'me':
            raise WrongData({'username': 'username "me" запрещен.'})
        data['username'] = data.get('username').lower()
        data['email'] = data.get('email').lower()
        return data
    
    def validate_login(self, data: OrderedDict) -> dict:
        """
        - Если пароль не правильный рейзим ошибку
        - Вносим данные о последнем логине пользователя
        """
        user = get_object_or_404(User, email=data.get('email'))
        if not check_password(data.get('password'), user.password):
            raise WrongData('Введены не правильные данные')
        user.last_login = timezone.now()
        user.save()
        return {'auth_token': get_tokens_for_user(user).get('access')}
    
    def validate_password(self, data: OrderedDict) -> OrderedDict:
        """
        - Проверка и смена пароля пользователя
        """
        user = get_object_or_404(User, username=self._args[0])
        if not check_password(data.get('current_password'), user.password):
            raise WrongData('Введен не правильный пароль')
        user.set_password(data.get('new_password'))
        user.save()
        return data

    def create_user(self, validated_data: dict) -> User:
        """Хешируем пароль через set_password."""
        user = User.objects.create(**validated_data)
        user.set_password(user.password)
        user.save()
        return user

    def is_subscribed(self, obj: Follow, request: Request) -> bool:
        return Follow.objects.filter(
            user=None if request.user.is_anonymous else request.user,
            following=obj).exists()
