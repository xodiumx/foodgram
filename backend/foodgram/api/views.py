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
from django_filters.rest_framework import DjangoFilterBackend

from django.shortcuts import get_list_or_404
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

from recipes.models import Tag, Ingredient
from .serializers import TagSerializer, IngredientSerializer
from .filters import IngredientFilter

class BaseUserViewSet(CreateModelMixin,
                      ListModelMixin,
                      RetrieveModelMixin,
                      GenericViewSet,):
    """Базовый ViewSet-для реализации CRUD."""
    ...


class TagViewSet(ListModelMixin,
                 RetrieveModelMixin,
                 GenericViewSet,):
    
    pagination_class = None
    http_method_names =('get',)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    

class IngredientViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    GenericViewSet,):

    pagination_class = None
    http_method_names =('get',)
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_class = IngredientFilter
