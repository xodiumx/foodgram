from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin, RetrieveModelMixin,
                                   UpdateModelMixin)
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView


from django.shortcuts import get_list_or_404
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

from recipes.models import Tag
from .serializers import TagSerializer

class BaseUserViewSet(CreateModelMixin,
                      ListModelMixin,
                      RetrieveModelMixin,
                      GenericViewSet,):
    """Базовый ViewSet-для реализации CRUD."""
    ...


class TagViewSet(ListModelMixin,
                 RetrieveModelMixin,
                 GenericViewSet,):
    
    serializer_class = TagSerializer
    http_method_names =('get',)
    pagination_class = None
    queryset = Tag.objects.all()