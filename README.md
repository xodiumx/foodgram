# Foodgram

![WorkflowBadge](https://github.com/xodiumx/foodgram/actions/workflows/foodgram_workflow.yml/badge.svg)

![Python](https://img.shields.io/badge/python-201933?style=for-the-badge&logo=python&logoColor=white) ![Celery](https://img.shields.io/badge/celery-201933?style=for-the-badge&logo=python&logoColor=white) ![Swagger](https://img.shields.io/badge/swagger-201933?style=for-the-badge&logo=python&logoColor=white) ![Redoc](https://img.shields.io/badge/redoc-201933?style=for-the-badge&logo=python&logoColor=white) ![PEP8](https://img.shields.io/badge/pep8-201933?style=for-the-badge&logo=python&logoColor=white) ![DjangoREST](https://img.shields.io/badge/DJANGO-REST-000000?style=for-the-badge&logo=django&logoColor=white&color=201933&labelColor=black) ![Postgres](https://img.shields.io/badge/postgresql-201933?style=for-the-badge&logo=postgresql&logoColor=white) ![Redis](https://img.shields.io/badge/redis-201933?style=for-the-badge&logo=redis&logoColor=white) ![Ubuntu](https://img.shields.io/badge/Ubuntu-201933?style=for-the-badge&logo=ubuntu&logoColor=white) ![Nginx](https://img.shields.io/badge/nginx-201933?style=for-the-badge&logo=nginx&logoColor=white) ![Docker](https://img.shields.io/badge/docker-201933?style=for-the-badge&logo=docker&logoColor=white) 

## Description

**Foodgram** «Продуктовый помощник», платформа на которой, вы можете создавать и делиться рецептами, у вас есть свой профиль и список избранного, а также есть возможность скачать все необходимые продукты для выбранных вами рецептов, одним кликом. *В проекте реализованы следующие возможности:*
 - Регистрация пользователей
 - Аутентификация пользователя через `JWT`
 - Создание и просмотр рецептов
 - Подписки на рецепты и на авторов
 - Страница избранного
 - Добавление рецептов в корзину
 - Загрузка всех продуктов из карзины в виде `pdf-file-a`

## Развернуть проект через `docker`
- перейдите в директорию `infra`
~~~
cd infra/
~~~
- создайте и заполните `.env` файл:
~~~
SECRET_KEY='django-insecure-a+=!1t6qxcq(k=m_$+dc0cwp73_2^k-%k)nht@1+0!f!-dw$%j'

DB_ENGINE=django.db.backends.postgresql
DB_NAME=foodgram
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

CSRF_TRUSTED_ORIGINS='http://localhost'

CELERY_BROKER_URL='redis://127.0.0.1:14000/0'
CELERY_RESULT_BACKEND='redis://127.0.0.1:14000/0'
CELERY_TASK_TRACK_STARTED=True
CELERY_TASK_TIME_LIMIT=60

ACCESS_TOKEN_LIFETIME=3
REFRESH_TOKEN_LIFETIME=12
ALGORITHM='HS256'
SLIDING_TOKEN_LIFETIME=5
SLIDING_TOKEN_REFRESH_LIFETIME=1

CORS_ALLOWED_ORIGINS='http://localhost'

~~~
- запустите команду:
~~~
docker-compose up -d
~~~
- В контейнере `db` выполните следующие команды: 
~~~
psql -U postgres
CREATE DATABASE foodgram;
~~~
- В контейнере `back` выполните следующую команду: 
~~~
python3 manage.py makemigrations --force-color -v 3 \
&& python3 manage.py migrate --force-color -v 3 \
&& python3 manage.py collectstatic \
&& python3 manage.py loaddata fixtures.json
~~~
- superuser - `admin:admin`
- user - `maks@example.com:maks1234`

## Загрузка данных из csv в БД

Чтобы загрузить данные из `ingredients.csv` в базу данных:
~~~
python manage.py import_data --load
~~~
Чтобы очистить базу данных:
~~~
python manage.py import_data --delete
~~~

## Алгоритм регистрации и авторизации пользователей
- Пользователь отправляет POST-запрос на эндпоинт `/api/users/`
~~~
{
  "email": "gordon@mail.com",
  "username": "gordon",
  "first_name": "Gordon",
  "last_name": "Ramzi",
  "password": "Qwerty123"
}
~~~
- Затем по эндпоинту `/api/auth/token/login/` пользователь отправляет email и пароль
~~~
{
  "email": "gordon@mail.com",
  "password": "Qwerty123"
}
~~~
- и получает токен авторизации
~~~
{
  "auth_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjgyMTY4Njc2LCJqdGkiOiIyNDJjNDczYTYwZGQ0YWJkYWIxNWExMTkyZjU2M2UzZiIsInVzZXJfaWQiOjJ9.gfF93gfcbxVFeaXlFoGL6Dw_1kqVTi0lRP5zn2zb7io"
}
~~~
- По эндпоинту `/api/auth/token/logout/` пользователь может выйти из своего профиля и токен попадет в `blacklist`
- Истекшие токены удаляются из базы раз в день, с помощью `celery tasks`

## Пример запроса к api на создание рецепта
- Авторизованный пользователь отправляет POST-запрос по эндпоинту `/api/recipes/` с данными о рецепте:
~~~
{
  "ingredients": [
    {
      "id": 2182,
      "amount": 4
    },
    {
      "id": 1081,
      "amount": 300
    },
    {
      "id": 1547,
      "amount": 100
    }
  ],
  "tags": [
    1,
    2
  ],
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
  "name": "Блины",
  "text": "Вкусные блины за 30 минут",
  "cooking_time": 30
}
~~~
- При успешном создании рецепта status 201
~~~
{
  "id": 1,
  "tags": [
    {
      "id": 1,
      "name": "Завтрак",
      "color": "#00c000",
      "slug": "breakfast"
    }
  ],
  "author": {
    "email": "gordon@mail.com",
    "id": 1,
    "username": "gordon",
    "first_name": "Gordon",
    "last_name": "Ramzi",
    "is_subscribed": false
  },
  "ingredients": [
    {
      "id": 0,
      "name": "Яйца куриные",
      "measurement_unit": "шт",
      "amount": 4
    }
    {
      "id": 1081,
      "name": "Мука",
      "measurement_unit": "г",
      "amount": 300
    },
    {
      "id": 1547,
      "name": "Сахар",
      "measurement_unit": "г",
      "amount": 100
    }
  ],
  "is_favorited": true,
  "is_in_shopping_cart": true,
  "name": "Блины",
  "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
  "text": "Вкусные блины за 30 минут",
  "cooking_time": 30
}
~~~

#### Более подробная документация доступна по эндпоинту `/api/docs/`

## Author - [Alekseev Maksim](https://t.me/maxalxeev)
