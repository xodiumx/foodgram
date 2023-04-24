from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from rest_framework.decorators import action
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin, RetrieveModelMixin,
                                   UpdateModelMixin)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED, HTTP_204_NO_CONTENT,
                                   HTTP_405_METHOD_NOT_ALLOWED)
from rest_framework.viewsets import GenericViewSet
from users.models import User

from foodgram.pagination import PagePaginationWithLimit

from .exceptions import CantAddTwice
from .filters import IngredientFilter, RecipeFilter
from .permissions import IsAuthorAndAuthenticatedOrReadOnly
from .serializers import (IngredientInfoSerializer, RecipeCreateSerializer,
                          RecipeSerializer, RecipeShortSerializer,
                          TagSerializer)
from .utils import get_shopping_cart


class TagViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet,):

    pagination_class = None
    http_method_names = ('get',)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet,):

    pagination_class = None
    http_method_names = ('get',)
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
    permission_classes = (IsAuthorAndAuthenticatedOrReadOnly,)

    @action(
        methods=('GET',),
        detail=False,
        filter_backends=None,
        pagination_class=None,
        url_path='download_shopping_cart',
        permission_classes=(IsAuthenticated,),)
    def download_shopping_cart(self, request):
        """
        Выдаем рецепт в виде pdf-file-a:
        - Создаем queryset Рецептов занесенных пользователем в корзину
        - Пердаем queryset в функцию формирования файла get_shopping_cart
        """
        user = get_object_or_404(User, id=request.user.id)
        queryset = ShoppingCart.objects.select_related(
            'recipe').filter(user=user)
        return get_shopping_cart(queryset)

    @action(
        methods=('POST', 'DELETE'),
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='(?P<id>\d+)/shopping_cart',)
    def shopping_cart(self, request, id):
        """
        Action for shopping_cart:
            - Если POST запрос, сериализуем recipe и создаем запись в Shopping
              если связь создана response - 201_created иначе рейзим ошибку
            - Если DELETE запрос удаляем запись в таблице Shopping по id и user
            - права доступа: авторизованные пользователи
            - доступные методы: POST, DELETE
        """
        if request.method == 'POST':
            recipe = get_object_or_404(Recipe, id=id)

            _, created = ShoppingCart.objects.get_or_create(
                recipe=recipe, user=request.user)
            
            if not created:
                raise CantAddTwice({'errors': 'Нельзя добавлять повторно'})

            serializer = RecipeShortSerializer(
                recipe, context={'request': request})
            return Response(serializer.data, HTTP_201_CREATED)
        
        if request.method == 'DELETE':
            get_object_or_404(
                ShoppingCart, user=request.user, recipe_id=id).delete()
            return Response(status=HTTP_204_NO_CONTENT)
        
        return Response(status=HTTP_405_METHOD_NOT_ALLOWED)

    @action(
        methods=('POST', 'DELETE'),
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='(?P<id>\d+)/favorite',)
    def favorite(self, request, id):
        """
        Action for subscribing:
            - Если POST запрос, сериализуем recipe и создаем запись в Favorite
              если связь создана response - 201_created иначе рейзим ошибку
            - Если DELETE запрос удаляем запись в таблице Favorite по id и user
            - права доступа: авторизованные пользователи
            - доступные методы: POST, DELETE
        """
        if request.method == 'POST':
            recipe = get_object_or_404(Recipe, id=id)

            _, created = Favorite.objects.get_or_create(
                recipe=recipe, user=request.user)
            
            if not created:
                raise CantAddTwice({'errors': 'Нельзя добавлять повторно'})
            
            serializer = RecipeShortSerializer(
                recipe, context={'request': request})
            return Response(serializer.data, HTTP_201_CREATED)
        
        if request.method == 'DELETE':
            get_object_or_404(
                Favorite, user=request.user, recipe_id=id).delete()
            return Response(status=HTTP_204_NO_CONTENT)

        return Response(status=HTTP_405_METHOD_NOT_ALLOWED)

    def get_serializer_class(self):
        if self.action in ('favorite', 'download_shopping_cart'):
            return None
        if self.action in ('list', 'retrieve'):
            return RecipeSerializer
        if self.action in ('create', 'partial_update'):
            return RecipeCreateSerializer
        return None

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
