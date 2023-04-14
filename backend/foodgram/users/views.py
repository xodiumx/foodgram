from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_list_or_404, get_object_or_404

from rest_framework.decorators import action
from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, RetrieveModelMixin,)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT,)
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

from .models import User, Follow
from .permissions import UserIsAuthenticated
from .serializers import (
        InfoSerializer,
        SignupSerializer,
        LoginSerializer,
        ChangePasswordSerializer,
        SubInfoSerializer,
        SubscriptionSerializer,)


class UserViewSet(CreateModelMixin,
                  ListModelMixin,
                  RetrieveModelMixin,
                  GenericViewSet,):
    
    lookup_field = 'id'
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    pagination_class = LimitOffsetPagination
    http_method_names = ('get', 'post', 'delete')

    @action(
        methods=('GET',),
        detail=False,
        permission_classes=(UserIsAuthenticated,),
        pagination_class=None,
        filter_backends=None,
        url_path='me',)
    def me(self, request):
        """
        Action for take info about your profile:
            - Права доступа: авторизованные пользователи.
            - requests methods - get
        """
        serializer = InfoSerializer(request.user,)
        return Response(serializer.data, status=HTTP_200_OK)

    @action(
        methods=('POST',),
        detail=False,
        permission_classes=(UserIsAuthenticated,),
        url_path='set_password',)
    def set_password(self, request):
        """
        Action for change password:
            - Права доступа: авторизованные пользователи.
            - requests methods - post
        """
        serializer = ChangePasswordSerializer(request.user, data=request.data,)
        serializer.is_valid(raise_exception=True)
        return Response(status=HTTP_204_NO_CONTENT)
    
    @swagger_auto_schema(
        method='post',
        manual_parameters=[
            openapi.Parameter(
                name='recipes_limit',
                in_=openapi.IN_QUERY,
                type='integer',
                required=False,
                description='how many recipes will be in request',
            )
        ],)
    @action(
        detail=False,
        methods=('POST', 'DELETE'),
        url_path='(?P<id>\d+)/subscribe',
        permission_classes=(UserIsAuthenticated, ),)
    def subscribe(self, request, id):
        """
        Action for subscribing:
            - Если POST запрос берем пользователя на которого подписываемся
              по id из url-a.
              Создаем запись в таблице Follow.
              Передаем объект following в сериализатор - SubInfoSerializer.

            - Если DELETE запрос берем объект из таблицы Follow, 
              отфильтрованный, по текущему user-у и following-у и удаляем его.

            - Права доступа: авторизованные пользователи.
            - requests methods - post, delete
        """
        current_user = request.user
        following = get_object_or_404(User, id=id)

        if request.method == 'POST':
            Follow.objects.create(user=current_user, following=following)
            serializer = SubInfoSerializer(following, 
                                           context={'request': request})
            return Response(serializer.data, HTTP_201_CREATED)
        
        elif request.method == 'DELETE':
            get_object_or_404(
                Follow, user=current_user, following=following).delete()
            return Response(status=HTTP_204_NO_CONTENT)
        
    @swagger_auto_schema(
        method = 'get',
        manual_parameters=[
            openapi.Parameter(
                name='recipes_limit',
                in_=openapi.IN_QUERY,
                type='integer',
                required=False,
                description='how many recipes will be in request',
            )
        ],)   
    @action(
        detail=False,
        methods=('GET',),
        url_path='subscriptions',
        permission_classes=(UserIsAuthenticated,),)
    def subscriptions(self, request):
        """
        Action for get subscriptions:
            - Получаем список id на которых подписан пользователь.
              Далее получаем queryset объектов User из этих id.
              Передаем в пагинацию, а затем сериализуем.

            - Права доступа: авторизованные пользователи.
            - requests methods - get
        """
        user = get_object_or_404(User, username=request.user.username)
        followed_id_list = user.follower.all().values_list(
            'following_id', flat=True
        )
        followed_users = User.objects.filter(id__in=followed_id_list).all()
        page = self.paginate_queryset(followed_users)
        serializer = SubscriptionSerializer(page, context={'request': request})
        return self.get_paginated_response(serializer.data)

    def get_serializer_class(self):
        if self.action == 'subscribe': return None
        elif self.action == 'subscriptions': return SubscriptionSerializer
        elif self.action == 'set_password': return ChangePasswordSerializer
        elif self.action in ('list', 'retrieve', 'me'): return InfoSerializer
        return SignupSerializer

    
class LoginViewset(TokenObtainPairView):
    """
    Login viewset:
        - права доступа - авторизованные пользователи
        - requests methods - post
    """
    http_method_names = ('post',)
    serializer_class = LoginSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, 
                        status=HTTP_201_CREATED)

class LogoutViewset(APIView):
    """
    Logout viewset:
        - права доступа - авторизованные пользователи
        - requests methods - post

    При logout-e достаем refresh-token-ы пользователя из таблицы
    OutstandingToken и заносим последний в blacklist
    """
    http_method_names = ('post',)
    permission_classes = (UserIsAuthenticated,)

    def post(self, request):
        tokens = get_list_or_404(OutstandingToken, user_id=request.user.id)
        refresh_token = RefreshToken(tokens[-1].token)
        refresh_token.blacklist()
        return Response(status=HTTP_204_NO_CONTENT)
