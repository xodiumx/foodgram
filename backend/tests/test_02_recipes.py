import pytest

from http import HTTPStatus


@pytest.mark.django_db(transaction=True)
class Test02RecipeAPI:
    recipes_get = '/api/recipes/'
    tags_get = '/api/recipes/'
    ingredients_get = '/api/recipes/'
    
    def test_00_recipes_get(self, client):
        response = client.get(self.recipes_get)
        assert response.status_code != HTTPStatus.NOT_FOUND, (
            f'Эндпоинт `{self.recipes_get}` не найден. Проверьте настройки '
            'в *urls.py*.'
        )

    def test_00_tags_get(self, client):
        response = client.get(self.tags_get)
        assert response.status_code != HTTPStatus.NOT_FOUND, (
            f'Эндпоинт `{self.tags_get}` не найден. Проверьте настройки '
            'в *urls.py*.'
        )
    
    def test_00_ingredients_get(self, client):
        response = client.get(self.ingredients_get)
        assert response.status_code != HTTPStatus.NOT_FOUND, (
            f'Эндпоинт `{self.ingredients_get}` не найден. Проверьте настройки '
            'в *urls.py*.'
        )