from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (
    CreateModelMixin, DestroyModelMixin,
    ListModelMixin, RetrieveModelMixin,
    UpdateModelMixin)
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT,)
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User, Follow
from .permissions import UserIsAuthenticated
from .serializers import (
        InfoSerializer,
        SignupSerializer,
        LoginSerializer,
        ChangePasswordSerializer,)

from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken


class BaseUserViewSet(CreateModelMixin,
                      ListModelMixin,
                      RetrieveModelMixin,
                      GenericViewSet,):
    """Базовый ViewSet-для реализации CRUD."""
    ...


class UserViewSet(BaseUserViewSet):
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    http_method_names = ('get', 'post', 'delete')
    permission_classes = (AllowAny,)
    pagination_class = LimitOffsetPagination
    lookup_field = 'id'

    @action(
        methods=('GET',),
        detail=False,
        permission_classes=(UserIsAuthenticated,),
        pagination_class=None,
        filter_backends=None,
        url_path='me')
    def me(self, request):
        serializer = InfoSerializer(
            request.user,
            data=request.data,
            partial=True)
        serializer.is_valid()
        return Response(serializer.data, status=HTTP_200_OK)

    @action(
        methods=('POST',),
        detail=False,
        permission_classes=(UserIsAuthenticated,),
        url_path='set_password')
    def set_password(self, request):
        serializer = ChangePasswordSerializer(
            request.user,
            data=request.data,)
        serializer.is_valid(raise_exception=True)
        return Response(status=HTTP_204_NO_CONTENT)
    
    @action(
        detail=False,
        methods=('POST', 'DELETE'),
        url_path='(?P<id>\d+)/subscribe',
        permission_classes=(UserIsAuthenticated,),)
    def subscribe(self, request, id):
        context = {}
        following = get_object_or_404(User, id=id)
        if request.method == 'POST':
            Follow.objects.create(user=request.user, following=following)
            context['email'] = following.email
            context['id'] = following.id
            context['username'] = following.username
            context['first_name'] = following.first_name
            context['last_name'] = following.last_name
            return Response(context, status=HTTP_201_CREATED)

    @action(
        detail=False,
        methods=('GET',),
        url_path='subscriptions',
        permission_classes=(UserIsAuthenticated,),)
    def subscriptions(self, request):
        ...

    def get_serializer_class(self):
        if self.action == 'subscribe': return None
        elif self.action == 'set_password': return ChangePasswordSerializer
        elif self.action in ('list', 'retrieve', 'me'): return InfoSerializer
        return SignupSerializer

  
class LoginViewset(TokenObtainPairView):
    
    serializer_class = LoginSerializer
    http_method_names = ('post',)


class LogoutViewset(APIView):
    
    permission_classes = (UserIsAuthenticated,)
    http_method_names = ('post',)

    def post(self, request):
        tokens = get_list_or_404(OutstandingToken, 
                                    user_id=request.user.id)
        refresh_token = RefreshToken(tokens[-1].token)
        refresh_token.blacklist()
        return Response(status=HTTP_204_NO_CONTENT)
    