FROM python:3.11.4-slim

RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Django-env
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=ttennis.settings.py

CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]