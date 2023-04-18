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
from django_filters.rest_framework import DjangoFilterBackend

from django.shortcuts import get_list_or_404

from foodgram.pagination  import PagePaginationWithLimit
from recipes.models import Tag, Ingredient, Recipe, AmountIngredient
from .serializers import (
    TagSerializer, IngredientInfoSerializer, RecipeSerializer,
    RecipeCreateSerializer, )
from .filters import IngredientFilter, RecipeFilter
from .permissions import UserIsAuthenticated


class TagViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet,):
    
    pagination_class = None
    http_method_names =('get',)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    

class IngredientViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet,):

    pagination_class = None
    http_method_names =('get',)
    queryset = Ingredient.objects.all()
    serializer_class = IngredientInfoSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_class = IngredientFilter


class RecipeViewSet(ListModelMixin, RetrieveModelMixin, CreateModelMixin,
                    DestroyModelMixin, UpdateModelMixin, GenericViewSet):
    
    queryset = Recipe.objects.prefetch_related(
        'ingredients__amountingredient_set').all()
    pagination_class = PagePaginationWithLimit
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    http_method_names = ('get', 'post', 'patch', 'delete')


    @action(
        methods=('GET',),
        detail=False,
        permission_classes=(UserIsAuthenticated,),
        url_path='download_shopping_cart',)
    def download_shopping_cart(self, request):
        ...
    
    @action(
        methods=('POST', 'DELETE'),
        detail=False,
        permission_classes=(UserIsAuthenticated,),
        url_path='(?P<id>\d+)/shopping_cart',)
    def shopping_cart(self, request):
        ...
    
    @action(
        methods=('POST', 'DELETE'),
        detail=False,
        permission_classes=(UserIsAuthenticated,),
        url_path='(?P<id>\d+)/favorite',)
    def favorite(self, request):
        ...

    
    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'): return RecipeSerializer
        elif self.action in ('create', 'partial_update'): 
            return RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
