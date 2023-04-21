import pytest

from http import HTTPStatus
from django.db.utils import IntegrityError

from tests.utils import (invalid_data_for_username_and_email_fields)


@pytest.mark.django_db(transaction=True)
class Test00UserRegistration:
    url_signup = '/api/users/'
    url_token = '/api/auth/token/login/'

    def test_00_nodata_signup(self, client):
        response = client.post(self.url_signup)

        assert response.status_code != HTTPStatus.NOT_FOUND, (
            f'Эндпоинт `{self.url_signup}` не найден. Проверьте настройки '
            'в *urls.py*.'
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f'Если POST-запрос, отправленный на эндпоинт `{self.url_signup}`, '
            'не содержит необходимых данных, должен вернуться ответ со '
            'статусом 400.'
        )

    def test_00_invalid_data_signup(self, client, django_user_model):
        invalid_data = {
            'email': 'invalid_email',
            'username': ' '
        }
        users_count = django_user_model.objects.count()

        response = client.post(self.url_signup, data=invalid_data)

        assert response.status_code != HTTPStatus.NOT_FOUND, (
            f'Эндпоинт `{self.url_signup}` не найден. Проверьте настройки '
            'в *urls.py*.'
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f'Если POST-запрос к эндпоинту `{self.url_signup}` содержит '
            'некорректные данные, должен вернуться ответ со статусом 400.'
        )
        assert users_count == django_user_model.objects.count(), (
            f'Проверьте, что POST-запрос к `{self.url_signup}` с '
            'некорректными данными не создаёт нового пользователя.'
        )

        response_json = response.json()
        invalid_fields = ('email', 'username')
        for field in invalid_fields:
            assert (field in response_json
                    and isinstance(response_json.get(field), list)), (
                f'Если в  POST-запросе к `{self.url_signup}` переданы '
                'некорректные данные, в ответе должна возвращаться информация '
                'о неправильно заполненных полях.'
            )

        valid_email = 'validemail@example.com'
        invalid_data = {
            'email': valid_email,
        }
        response = client.post(self.url_signup, data=invalid_data)
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f'Если POST-запрос к `{self.url_signup}` не содержит '
            'данных о `username`, должен вернуться ответ со статусом 400.'
        )
        assert users_count == django_user_model.objects.count(), (
            f'Проверьте, что POST-запрос к `{self.url_signup}`, не содержащий '
            'данных о `username`, не создаёт нового пользователя.'
        )

    @pytest.mark.parametrize(
        'data,messege', invalid_data_for_username_and_email_fields
    )
    def test_00_singup_length_and_simbols_validation(self, client,
                                                     data, messege,
                                                     django_user_model):
        request_method = 'POST'
        users_count = django_user_model.objects.count()
        response = client.post(self.url_signup, data=data)
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            messege[0].format(
                url=self.url_signup, request_method=request_method
            )
        )
        assert django_user_model.objects.count() == users_count, (
            f'Если в POST-запросе к эндпоинту `{self.url_signup}` '
            'значения полей не соответствуют ограничениям по длине или '
            'содержанию - новый пользователь не должен быть создан.'
        )

    def test_00_valid_data_user_signup(self, client, django_user_model):
        valid_data = {
            'email': 'maks@example.com',
            'password': '12345',
            'first_name': 'Maks',
            'last_name': 'Alekseev',
            'username': 'maks',
        }
        valid_data_after_signup = {
            'email': 'maks@example.com',
            'first_name': 'Maks',
            'last_name': 'Alekseev',
            'username': 'maks',
            'id': 1,
        }

        response = client.post(self.url_signup, data=valid_data)

        assert response.status_code != HTTPStatus.NOT_FOUND, (
            f'Эндпоинт `{self.url_signup}` не найден. Проверьте настройки '
            'в *urls.py*.'
        )
        assert response.status_code == HTTPStatus.CREATED, (
            'POST-запрос с корректными данными, отправленный на эндпоинт '
            f'`{self.url_signup}`, должен вернуть ответ со статусом 201.'
        )
        assert response.json() == valid_data_after_signup, (
            'POST-запрос с корректными данными, отправленный на эндпоинт '
            f'`{self.url_signup}`, должен вернуть ответ, содержащий '
            'информацию о {valid_data_after_signup} созданного пользователя.'
        )

        new_user = django_user_model.objects.filter(email=valid_data['email'])
        assert new_user.exists(), (
            'POST-запрос с корректными данными, отправленный на эндпоинт '
            f'`{self.url_signup}`, должен создать нового пользователя.'
        )
        new_user.delete()
    

    def test_00_obtain_jwt_token_invalid_data(self, client):
        response = client.post(self.url_token)
        assert response.status_code != HTTPStatus.NOT_FOUND, (
            f'Эндпоинт `{self.url_token}` не найдена. Проверьте настройки в '
            '*urls.py*.'
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            'Проверьте, что POST-запрос без данных, отправленный на эндпоинт '
            f'`{self.url_token}`, возвращает ответ со статусом 400.'
        )
        invalid_data = {
            'email': 'notemail',
            'password': '    ',
        }
        response = client.post(self.url_token, data=invalid_data)
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            'Проверьте, что POST-запрос, отправленный на эндпоинт '
            f'`{self.url_token}`и не содержащий информации о `email`, и '
            '`password` возвращает ответ со статусом 400.'
        )
        invalid_data = {
            'email': 'unexisting_mail@mail.com',
            'password': '123452134431'
        }
        response = client.post(self.url_token, data=invalid_data)
        assert response.status_code == HTTPStatus.NOT_FOUND, (
            'Проверьте, что POST-запрос с несуществующим `email`, '
            f'отправленный на эндпоинт `{self.url_token}`, возвращает ответ '
            'со статусом 404.'
        )
        invalid_data = {
            'email': 'maks@example.com',
            'password': '12312312'
        }
        response = client.post(self.url_token, data=invalid_data)
        assert response.status_code == HTTPStatus.NOT_FOUND, (
            'Проверьте, что POST-запрос с корректным `mail` и невалидным '
            f'`password`, отправленный на эндпоинт `{self.url_token}`'
            ', возвращает ответ со статусом 404.'
        )


    def test_00_registration_same_email_restricted(self, client):
        first_user = {
            'email': 'maks@example.com',
            'password': '12345',
            'first_name': 'Maks',
            'last_name': 'Alekseev',
            'username': 'maks',
        }
        second_user = {
            'email': 'maks@example.com',
            'password': '12345',
            'first_name': 'Maks',
            'last_name': 'Alekseev',
            'username': 'maks1',
        }
        response = client.post(self.url_signup, data=first_user)
        assert response.status_code == HTTPStatus.CREATED, (
            f'Проверьте, что POST-запрос к `{self.url_signup}` с корректными '
            'возвращает статус-код 201.'
        )

        assert_msg = (
            f'Если POST-запрос, отправленный на эндпоинт `{self.url_signup}`, '
            'содержит `email` зарегистрированного пользователя и незанятый '
            '`username` - должен вернуться ответ со статусом 400.'
        )
        try:
            response = client.post(self.url_signup, data=second_user)
        except IntegrityError:
            raise AssertionError(assert_msg)
        assert response.status_code == HTTPStatus.BAD_REQUEST, (assert_msg)
