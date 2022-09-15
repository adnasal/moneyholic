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
def collect_articles() -> str:
    create_default_symbols()
    symbols = Symbol.objects.all()
    url: str = 'https://feeds.finance.yahoo.com/rss/2.0/headline?s='
    other_params = '&region=US&lang=en-US'

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
                    'published_at': article.find('pubDate').text,
                    'symbol': symbol_id
                }

                articles_list.append(article)

            for article in articles_list:

                existing_article = Article.objects.filter(external_id=article.get('external_id'))

                if not existing_article:
                    serializer = ArticleSerializer(data=article)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                else:
                    serializer = ArticleSerializer(instance=Article.objects.get(
                        external_id__exact=article.get('external_id')),
                        data=article)
                    serializer.is_valid()
                    serializer.save()

        return "Done"
