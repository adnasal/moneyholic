import datetime
from datetime import date, timedelta, datetime

import requests
from bs4 import BeautifulSoup
from celery import shared_task

from django.conf import settings

from newscraper.celery import app
from newscraper.top_15_words.filter_string import filter_string
from newscraper.top_15_words.map_reduce import map_string, reduce
from newscraper.top_15_words.saver import save_to_db
from .models import Article, Symbol, Wordcount
from .serializers import ArticleSerializer

today = date.today()


@shared_task(name='CollectArticlesYahoo')
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
                title = article.get('title')
                count_words(title)

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


@shared_task(name='ArchiveArticles')
def archive_articles(days=30) -> str:
    Article.objects.filter(published_at__lte=today - timedelta(days=days)).update(is_archived=True)

    return "Done"


@shared_task(name='DeleteArticles')
def delete_articles(days=90) -> str:
    Article.objects.filter(published_at__lte=today - timedelta(days=days)).update(is_deleted=True)

    return "Done"


@shared_task(name='PurgeCeleryQueue')
def purge_celery_queue() -> str:
    app.control.purge()

    return "Done"


def count_words(title) -> str:
    mapped = map_string(filter_string(title))
    save_to_db(reduce(mapped))

    return "Done"


@shared_task(name='TopKeywords')
def save_keywords(keywords=Wordcount.objects.all()):
    my_dict = {}
    for keyword in keywords:
        my_dict[keyword.word] = keyword.count

    top_15_keywords = sorted(my_dict, key=my_dict.get, reverse=True)[:15]

    for keyword in top_15_keywords:
        top_15_keywords = Wordcount.objects.filter(word=keyword).update(is_keyword=True)

    return top_15_keywords
