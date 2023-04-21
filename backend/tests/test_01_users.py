import pytest

from http import HTTPStatus


@pytest.mark.django_db(transaction=True)
class Test01UserAPI:
    set_password = '/api/users/set_password/'
    logout = '/api/auth/token/logout/'
    me = '/api/users/me/'
    users = '/api/users/'

    VALID_DATA_FOR_USER_CREATION = [
        (
            {
            'email': 'maks@example.com',
            'password': '12345',
            'first_name': 'Maks',
            'last_name': 'Alekseev',
            'username': 'maks',
            },
        ),
    ]
    PATCH_DATA = {
        'new_password': '1234',
        'current_password': '12345'
    }

    def test_01_users_not_authenticated(self, client):
        response = client.get(self.users)

        assert response.status_code != HTTPStatus.NOT_FOUND, (
            'Эндпоинт `/api/users/` не найден. Проверьте настройки в '
            '*urls.py*.'
        )

        assert response.status_code == HTTPStatus.OK, (
            'Проверьте, что GET-запрос к `/api/users/` без токена '
            'авторизации возвращается ответ со статусом 200.'
        )


    def test_02_users_id_authenticated(self, user_client, user):
        user_id = user.id
        response = user_client.get(f'/api/users/{user_id}/')

        assert response.status_code != HTTPStatus.NOT_FOUND, (
            f'Эндпоинт `/api/users/{user_id}/` не найден. Проверьте '
            'настройки в *urls.py*.'
        )
        assert response.status_code == HTTPStatus.OK, (
            f'Проверьте, что GET-запрос `/api/v1/users/{user_id}/` с '
            'токеном авторизации возвращает ответ со статусом 200.'
        )


    def test_03_users_me_not_authenticated(self, client):
        response = client.get(self.me)

        assert response.status_code != HTTPStatus.NOT_FOUND, (
            f'Эндпоинт `{self.me}` не найден. Проверьте настройки '
            'в *urls.py*.'
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            f'Проверьте, что GET-запрос `{self.me}` без токена '
            'авторизации возвращает ответ со статусом 401.'
        )


    def test_04_set_password(self, user_client, user):
        response = user_client.put(
            self.set_password, data=self.PATCH_DATA
        )
        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED, (
            f'Проверьте, что PUT-запрос к `{self.set_password}` '
            'не предусмотрен и возвращает статус 405.'
        )
        response = user_client.post(self.set_password, data=self.PATCH_DATA)
        assert response.status_code == HTTPStatus.NO_CONTENT, (
            f'Проверьте, что POST-запрос к `{self.set_password}` с корректными'
            ' возвращает статус-код 204.'
        )


    def test_06_users_me_get(self, user_client, user):
        response = user_client.get(self.me)
        assert response.status_code == HTTPStatus.OK, (
            'Проверьте, что GET-запрос обычного пользователя к '
            '`/api/v1/users/me/` возвращает ответ со статусом 200.'
        )

        response_data = response.json()
        expected_keys = ('username', 'id', 'email', 'first_name', 'last_name',)
        for key in expected_keys:
            assert response_data.get(key) == getattr(user, key), (
                f'Проверьте, что GET-запрос к `{self.me}` возвращает '
                'данные пользователя в неизмененном виде. Сейчас ключ '
                f'`{key}` отсутствует либо содержит некорректные данные.'
            )

    def test_06_02_users_me_delete_not_allowed(self, user_client, user,
                                               django_user_model):
        response = user_client.delete(self.me)
        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED, (
            f'Проверьте, что DELETE-запрос к `{self.me}` возвращает '
            'ответ со статусом 405.'
        )
        user = (
            django_user_model.objects.filter(username=user.username).first()
        )
        assert user, (
            f'Проверьте, что DELETE-запрос к `{self.me}` не удаляет '
            'пользователя.'
        )

    def test_06_02_users_me_update_not_allowed(self, user_client, user,
                                               django_user_model):
        response = user_client.patch(self.me)
        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED, (
            f'Проверьте, что PATCH-запрос к `{self.me}` возвращает '
            'ответ со статусом 405.'
        )
        response = user_client.put(self.me)
        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED, (
            f'Проверьте, что PUT-запрос к `{self.me}` возвращает '
            'ответ со статусом 405.'
        )
