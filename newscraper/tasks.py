import requests
from bs4 import BeautifulSoup
from celery import task

from .models import Article, Symbol
from .serializers import ArticleSerializer, SymbolSerializer


def create_default_symbols():
    symbols = Symbol.objects.all()
    if not symbols:
        default_symbols = [
            {
                'symbol': 'INTC'
            },
            {
                'symbol': 'AAPL'
            },
            {
                'symbol': 'TWTR'
            },
            {
                'symbol': 'GC=F'
            }
        ]
        for new_symbol in default_symbols:
            serializer = SymbolSerializer(data=new_symbol)
            serializer.is_valid(raise_exception=True)
            serializer.save()


@task(name='CollectArticles')
def collect_articles():

    create_default_symbols()
    symbols = Symbol.objects.all()
    url = 'https://feeds.finance.yahoo.com/rss/2.0/headline?s='
    other_params = '&region=US&lang=en-US'

    for s in symbols:
        get_articles = requests.get(''.join([url, s.symbol, other_params]), headers={'User-agent': 'Mozilla/5.0'}).content
        soup = BeautifulSoup(get_articles, 'xml')
        articles = soup.find_all('item')
        articles_list = []
        symbol_id = s.id

        for a in articles:
            article = {
                'title': a.find('title').text,
                'text': a.find('description').text,
                'article_link': a.find('link').text,
                'external_id': a.find('guid').text,
                'published_at': a.find('pubDate').text,
                'symbol': symbol_id
            }

            articles_list.append(article)

        for i in articles_list:

            existing_article = Article.objects.filter(external_id=i.get('external_id'))

            if not existing_article:
                serializer = ArticleSerializer(data=i)
                serializer.is_valid(raise_exception=True)
                serializer.save()
            else:
                serializer = ArticleSerializer(instance=Article.objects.get(external_id__exact=i.get('external_id')), data=i)
                serializer.is_valid()
                serializer.save()

    return "Done"
