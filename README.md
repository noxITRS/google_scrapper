# Google Scrapper

A small web application for google scrapping.

## Installation

To easy run application clone (or download) repository

Get docker from:

https://www.docker.com/get-started

After that create .env.prod file in root directory,

example of .env.prod:

```bash
DEBUG=0
SECRET_KEY=your_secret_key
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=google_scrapper_prod
SQL_USER=django_sql
SQL_PASSWORD=django_sql
SQL_HOST=postgres
SQL_PORT=5432
DATABASE=postgres
```


If you want to define cache time by yourself add CACHE_TTL environment variable, for example
```bash
CACHE_TTL=60*15
```
caches page view for 15 minutes.


Create .env.prod.db file also in root directory


example of .env.prod.db:
```bash
POSTGRES_USER=django_sql
POSTGRES_PASSWORD=django_sql
POSTGRES_DB=google_scrapper_prod
```

Write below command to build and run container:
```bash
docker-compose -f docker-compose.prod.yml up -d --build
```

Run database migrations:
```bash
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput
```

## Usage

To try application open http://localhost:1337/

## Stop

To stop container type:
```bash
docker-compose -f docker-compose.prod.yml down -v
```
