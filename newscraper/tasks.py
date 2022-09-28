import datetime
from datetime import date, timedelta, datetime

import requests
from bs4 import BeautifulSoup
from celery import task
from django.conf import settings

from newscraper.celery import app
from .models import Article, Symbol
from .serializers import ArticleSerializer

today = date.today()


@task(name='CollectArticlesYahoo')
def collect_articles_yahoo() -> str:
    symbols = Symbol.objects.filter(is_enabled=True)
    url: str = settings.SCRAPING_URL
    other_params = settings.US

    if symbols:
        for symbol in symbols:
            get_articles = requests.get(''.join([url, symbol.symbol, other_params]),
                                        headers={'User-agent': 'Mozilla/5.0'}).content
            soup = BeautifulSoup(get_articles, 'xml')
            articles = soup.find_all('item')
            articles_list = []
            symbol_id = symbol.id

            for article in articles:
                article = {
                    'title': article.find('title').text,
                    'text': article.find('description').text,
                    'article_link': article.find('link').text,
                    'external_id': article.find('guid').text,
                    'published_at': datetime.strptime(article.find('pubDate').text, '%a, %d %b %Y %H:%M:%S %z'),
                    'symbol': symbol_id,
                    'is_archived': False,
                    'is_deleted': False,
                }

                articles_list.append(article)

            for article in articles_list:

                existing_article = Article.objects.filter(external_id=article.get('external_id'),
                                                          symbol__is_enabled=True)

                if not existing_article:
                    serializer = ArticleSerializer(data=article)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                else:
                    serializer = ArticleSerializer(instance=Article.objects.get(
                        external_id__exact=article.get('external_id'), symbol__is_enabled=True),
                        data=article)
                    serializer.is_valid()
                    serializer.save()

        return "Done"


@task(name='ArchiveArticles')
def archive_articles(days=30) -> str:
    last_month = today - timedelta(days=days)
    Article.objects.filter(published_at__lte=last_month).update(is_archived=True)

    return "Done"


@task(name='DeleteArticles')
def delete_articles(days=90) -> str:
    last_three_months = today - timedelta(days=days)
    Article.objects.filter(published_at__lte=last_three_months).update(is_deleted=True)

    return "Done"


@task(name='PurgeCeleryQueue')
def purge_celery_queue() -> str:
    app.control.purge()

    return "Done"
