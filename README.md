# Foodgram

![](https://github.com/xodiumx/foodgram/actions/workflows/foodgram_workflow.yml/badge.svg)

![Python](https://img.shields.io/badge/python-201933?style=for-the-badge&logo=python&logoColor=white) ![DjangoREST](https://img.shields.io/badge/DJANGO-REST-000000?style=for-the-badge&logo=django&logoColor=white&color=201933&labelColor=black) ![Swagger](https://img.shields.io/badge/swagger-201933?style=for-the-badge&logo=python&logoColor=white) ![Redoc](https://img.shields.io/badge/redoc-201933?style=for-the-badge&logo=python&logoColor=white) ![Postgres](https://img.shields.io/badge/postgresql-201933?style=for-the-badge&logo=postgresql&logoColor=white) ![Redis](https://img.shields.io/badge/redis-201933?style=for-the-badge&logo=redis&logoColor=white) ![Ubuntu](https://img.shields.io/badge/Ubuntu-201933?style=for-the-badge&logo=ubuntu&logoColor=white) ![Nginx](https://img.shields.io/badge/nginx-201933?style=for-the-badge&logo=nginx&logoColor=white) ![Docker](https://img.shields.io/badge/docker-201933?style=for-the-badge&logo=docker&logoColor=white)

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
