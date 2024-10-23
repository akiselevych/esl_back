# ESL API Documentation

## Backend requirements
* <a href="https://www.docker.com/" style="text-decoration: underline; font-size: 15px">Docker</a>
* <a href="https://docs.docker.com/compose/install/" style="text-decoration: underline; font-size: 15px">Docker Compose</a>
* <a href="https://python-poetry.org/" style="text-decoration: underline; font-size: 15px">Poetry</a> for python package and environment management

## The .env files

First of all, you have to create all necessary .env files

* `.env` file with global information for project
```
DEBUG=True
```

By default `DEBUG` is **True**. If you want to start a project not in a `DEBUG` mode, you should change `DEBUG` to **False**

* `.env.dev` file with variables and values for development mode

```
# DATABASE
DATABASE_URL=

DB_NAME=esl # default name, you can set another
DB_USER=postgres
DB_PASSWORD=password # default password
DB_HOST=postgres-db
DB_PORT=5432 # default port

# PG ADMIN SETTINGS
PG_ADMIN_EMAIL=esl_admin@gmail.com # example
PG_ADMIN_PASSWORD=admin # example

# ORIGINS
CORS_ORIGINS=[http://localhost:3000, http://localhost] # example list

# APP
APP_NAME=
APP_VERSION=
```

### Database

`DATABASE_URL` - optional variable. If you won't provide it, it will be constructed from other Database connection variables. If you want to provide your custom `DATABASE_URL`, you will need to provide <a href="https://docs.sqlalchemy.org/en/20/glossary.html#term-DBAPI" style="text-decoration: underline; font-size: 15px">DBAPI</a> url for sqlalchemy database connection, e.g: `postgresql+psycopg_async://postgres:password@postgres-db:5432/esl?async_fallback=true` - postgresql async connection with async psycopg3

`DB_NAME` - database name

`DB_USER` - database user

`DB_PASSWORD` - database password

`DB_HOST` - database host, you should provide `postgres-db` here if you are starting the project with Docker Compose, or if you want your custom value for this field, you need to change it in the `docker-compose.dev.yml` if you are starting the project for development, or in the `docker-compose.prod.yml` if you are starting the project for production

`DB_PORT` - you can provide default `5432` or another value for port

### PgAdmin

`PG_ADMIN_EMAIL` - email for pg admin account. You will need to use it to enter the panel using this link: http://localhost:82

`PG_ADMIN_PASSWORD` - password for account

### CORS Origins

`CORS_ORIGINS` - the list with websites, which you want to allow to use this API. You should provide them in this format: `[http://localhost:3000, http://localhost]`

### App

`APP_NAME` - optional variable, you can remove it or leave it empty, and in this case `APP_NAME` will be "Project API". Or you can provide your value for `APP_NAME` variable and it will be set instead of default

`APP_VERSION` - optional variable too. If you won't provide it, by default will be set `1` and final prefix of app version for the all urls will be `/api/v1`. Or you can provide your value, but it must be an `integer`


## Backend local development
*  Build project with Docker Compose:
```
docker compose --env-file .env.dev -f docker-compose.dev.yml build
```

* And after build you can start it
```
docker compose --env-file .env.dev -f docker-compose.dev.yml up -d
```

You can access to the backend app on the path: http://localhost:8000

Automatic interactive documentation with Swagger UI: http://localhost:8000/docs

Alternative automatic documentation with ReDoc: http://localhost:8000/redoc

PGAdmin, PostgreSQL web administration: http://localhost:82

To check the logs, run:
```
docker compose -f docker-compose.dev.yml logs
```

To check the logs of a specific service, add the name of the service, e.g.:

```
docker compose -f docker-compose.dev.yml logs api
```