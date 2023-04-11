from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import check_password

from rest_framework.serializers import (
    CharField, EmailField, ModelSerializer,
    Serializer, SlugRelatedField, 
    CurrentUserDefault, Field)

from .models import User
from .utils import get_tokens_for_user
from .exceptions import WrongData


class InfoSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',)

    
class SignupSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name',)

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(user.password)
        user.save()
        return user


class LoginSerializer(Serializer):

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

    new_password = CharField(max_length=64)
    current_password = CharField(max_length=64)

    def validate(self, data):
        user = get_object_or_404(User, username=self._args[0])
        if not check_password(data.get('current_password'), user.password):
            raise WrongData('Введен не правильный пароль')
        user.set_password(data.get('new_password'))
        user.save()
        return data
