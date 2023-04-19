FROM python:3.10.11

WORKDIR /app

RUN pip3 install --upgrade pip

COPY requirements.txt .

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000"]

LABEL author="Alekseev Maksim" version=1.0