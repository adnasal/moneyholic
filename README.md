# Moneyholic

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Moneyholic is Django based REST api service for financial news. Service has two parts: REST api service and scraping service. REST api is used for fetching data and scraping service collects and stores data from Yahoo finance site. 

## Highlights

Moneyholic works with help of five different services, which can be seen in docker-compose.yml file:

- db (Postgresql)
- web
- worker (Celery)
- scheduler (celery.beat)
- message broker and cache (Redis)
- flower (Flower as Celery dashboard with authentication)

### Features built-in

All needed environment variables can be found in .env file.

Project is dockerized; services are run in Docker containers, virtual environment and all the requirements can be found under /requirements directory.

This api collects all kinds of financial news form Yahoo Finance site, but primarily has 4 different symbols news can be
distincted upon: AATL, TWTR, GC=F and INTC.

This api consists of next endpoints (url.py), Postman collection tested:

- News
- Recent News (News from previous day)
- News Per Symbol
- News Per Symbol Class
- News Per Search (keyword), date, date_from, date_to
- Archived News
- Deleted News
- List Symbols
- Add Symbol
- Update Symbol
- Remove Symbol*
- Get Article
- Remove Article**
- Delete Article
- Archive Article
- Add Comment
- Delete Comment
- See Comments
- Wordcount (MapReduce)
- Top 15 Keywords
- Top 5 most liked articles
- Top 5 most commented articles
- Top 5 most liked comments

Symbol can be removed only if all of its connected articles are removed. Only for admin purposes.

## API Docs

API documentation is automatically generated using Swagger. You can view documention by visiting this [link](http://localhost:8000/swagger).

Symbol can be enabled or disabled. Only enabled symbols' articles will be shown on news feed.

GetOrNone manager was implemented in order to avoid using filter method in cases where None response was desired and there was only one object to work with.

Validations were done on views, such as:

- Already existing symbol cannot be added
- Article/symbol that does not exist cannot be removed
- Already archived/deleted articles cannot be archived/deleted again
- Appropriate messages when errors happen
- Cannot delete default symbols (AATL,TWTR, GC=F and INTC)

Pagination is implemented, and can be checked by setting page query param, for example:
Invalidated caching is implemented.

http://localhost:8000/api/v1/news/?symbol=TWTR&&page=2

This would return all the news with symbol TWTR positioned on page 2.

Celery is used for asynchronous tasks and periodic scraping every 15 minutes, with initial scrape starting when the app starts. Library used for scraping is BeautifulSoup4.

News are per default archived when 30 days old, and deleted when 90 days old. These values can be changed in Django Admin.
Queue is per default purged every day to keep the working flow clean.
## Admin dashboard

Admin page for this app can be visited [here].(http://localhost:8000/admin/newscraper)

## Task dashboard
Flower page for this app with all the tasks can be visited [here].(http://localhost:5555/tasks)

## Prerequisites

If you are familiar with Docker, then you just need [Docker](https://docs.docker.com/docker-for-mac/install/). If you don't want to use Docker, then you just need Python3 and Postgres installed.

## Setup

After cloning the project and navigating to the cloned project, run the following command:

```bash
docker-compose up
```
Afterwards, you should see 6 running containers.

## Local Development with Docker

Start the dev server for local development:

```bash
cp .env.dist .env
docker-compose up
```

Run a command inside the docker container:

```bash
docker-compose run --rm web [command]
```

## Local Development without Docker

### Install

```bash
python3 -m venv env && source env/bin/activate                # activate venv
cp .env.dist .env                                             # create .env file and fill-in DB info
pip install -r requirements.txt                               # install py requirements
./manage.py migrate                                           # run migrations
./manage.py collectstatic --noinput                           # collect static files
redis-server                                                  # run redis locally for celery
celery -A src.config worker --beat --loglevel=debug
  --pidfile="./celerybeat.pid"
  --scheduler django_celery_beat.schedulers:DatabaseScheduler # run celery beat and worker
```

### Run dev server

This will run server on [http://localhost:8000](http://localhost:8000)

```bash
python3 manage.py runserver
```

### Create superuser

If you want, you can create initial super-user with next commad:

```bash
python3 manage.py createsuperuser
```

### Running Tests

Unit tests and model factories for most important code parts are written and can be run by the following command, with coverage integrated:

```bash
python3 manage.py test
```

