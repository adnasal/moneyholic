import requests
from bs4 import BeautifulSoup
from celery import task

from .models import Article, Symbol
from .serializers import ArticleSerializer, SymbolSerializer


@task(name='TestTask')
def send_email_task():
    return 3+3


def create_default_symbols():

    symbols = Symbol.objects.all()
    if len(symbols) is 0:
        default_symbols = [
            {
                'symbol': 'AAPL'
            },
            {
                'symbol': 'TWTR'
            },
            {
                'symbol': 'GC=F'
            },
            {
                'symbol': 'INTC'
            }
        ]
        for i in default_symbols:
            serializer = SymbolSerializer(data=i)
            serializer.is_valid(raise_exception=True)
            serializer.save()


@task(name='CollectArticles')
def collect_articles():

    create_default_symbols()
    symbols = Symbol.objects.all()
    url = 'https://feeds.finance.yahoo.com/rss/2.0/headline?s='
    other_params = '&region=US&lang=en-US'

    for j in symbols:
        get_articles = requests.get(url + j.symbol + other_params, headers={'User-agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(get_articles.content, features='xml')
        articles = soup.findAll('item')
        articles_list = []
        symbol_id = j.id

        for a in articles:
            article = {
                'title': a.find('title').text,
                'text': a.find('description').text,
                'article_link': a.find('link').text,
                'published_at': a.find('pubDate').text,
                'symbol': symbol_id
            }

            articles_list.append(article)

        for i in articles_list:

            existing_article = Article.objects.get_or_none(external_id=i.get('external_id'))

            if existing_article is None:
                serializer = ArticleSerializer(data=i)
                serializer.is_valid(raise_exception=True)
                serializer.save()
            else:
                serializer = ArticleSerializer(instance=Article.objects.get(external_id__exact=i.get('external_id')), data=i)
                serializer.is_valid()
                serializer.save()

    return "Done"
