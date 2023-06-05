from django.shortcuts import get_list_or_404, get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.mixins import (CreateModelMixin, ListModelMixin,
                                   RetrieveModelMixin)
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_204_NO_CONTENT,
                                   HTTP_405_METHOD_NOT_ALLOWED)
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from foodgram.pagination import PagePaginationWithLimit

from .exceptions import CantSubscribe, UserIsNotAuthenticated
from .models import Follow, User
from .permissions import UserIsAuthenticated
from .serializers import (ChangePasswordSerializer, InfoSerializer,
                          LoginSerializer, SignupSerializer, SubInfoSerializer,
                          SubscriptionSerializer)


class UserViewSet(CreateModelMixin,
                  ListModelMixin,
                  RetrieveModelMixin,
                  GenericViewSet,):

    lookup_field = 'id'
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    pagination_class = PagePaginationWithLimit
    http_method_names = ('get', 'post', 'delete')

    @action(
        methods=('GET',),
        detail=False,
        permission_classes=(UserIsAuthenticated,),
        pagination_class=None,
        filter_backends=None,
        url_path='me',)
    def me(self, request: Request) -> Response:
        """
        Action for take info about your profile:
            - Права доступа: авторизованные пользователи.
            - requests methods - get
        """
        serializer = InfoSerializer(request.user, context={'request': request})
        return Response(serializer.data, status=HTTP_200_OK)

    @action(
        methods=('POST',),
        detail=False,
        permission_classes=(UserIsAuthenticated,),
        url_path='set_password',)
    def set_password(self, request: Request) -> Response:
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
    def subscribe(self, request: Request, id: str) -> Response:
        """
        Action for subscribing:
            - Если POST запрос берем пользователя на которого подписываемся
              по id из url-a.
              Если current_user == followin рейзим ошибку
              Создаем запись в таблице Follow.
              Если запись о подписке уже создана рейзим ошибку
              Передаем объект following в сериализатор - SubInfoSerializer.

            - Если DELETE запрос берем объект из таблицы Follow,
              отфильтрованный, по текущему user-у и following-у и удаляем его.

            - Права доступа: авторизованные пользователи.
            - requests methods - post, delete
        """
        current_user = request.user
        following = get_object_or_404(User, id=id)

        if request.method == 'POST':
            if current_user == following:
                raise CantSubscribe({'errors': 'Нельзя подписаться на себя'})
            
            _, created = Follow.objects.get_or_create(
                user=current_user, following=following)
            if not created:
                raise CantSubscribe({'errors': 'Нельзя подписаться повторно'})
            
            serializer = SubInfoSerializer(following,
                                           context={'request': request})
            return Response(serializer.data, HTTP_201_CREATED)
        
        if request.method == 'DELETE':
            get_object_or_404(
                Follow, user=current_user, following=following).delete()
            return Response(status=HTTP_204_NO_CONTENT)
        
        return Response(status=HTTP_405_METHOD_NOT_ALLOWED)

    @swagger_auto_schema(
        method='get',
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
    def subscriptions(self, request: Request) -> Response:
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
        if self.action == 'subscribe':
            return None
        if self.action == 'subscriptions':
            return SubscriptionSerializer
        if self.action == 'set_password':
            return ChangePasswordSerializer
        if self.action == 'list':
            return InfoSerializer
        if self.action in ('retrieve', 'me'):
            if not self.request.user.is_anonymous:
                return InfoSerializer
            raise UserIsNotAuthenticated(
                {'detail': 'Учетные данные не были предоставлены.'})
        return SignupSerializer


class LoginViewset(TokenObtainPairView):
    """
    Login viewset:
        - права доступа - авторизованные пользователи
        - requests methods - post
    """
    http_method_names = ('post',)
    serializer_class = LoginSerializer

    def post(self, request: Request) -> Response:
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

    def post(self, request: Request) -> Response:
        tokens = get_list_or_404(OutstandingToken, user_id=request.user.id)
        refresh_token = RefreshToken(tokens[-1].token)
        refresh_token.blacklist()
        return Response(status=HTTP_204_NO_CONTENT)
