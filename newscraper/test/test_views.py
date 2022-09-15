from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APIRequestFactory

from newscraper.models import Symbol, Article
from newscraper.test.factories import SymbolFactory, ArticleFactory

factory = APIRequestFactory()


class TestViews(TestCase):
    symbol = SymbolFactory()
    article = ArticleFactory()
    client = Client()

    def test_list_symbols(self):
        response = self.client.get(reverse('symbols'))

        self.assertEquals(response.status_code, 200)

    def test_add_symbol(self):
        response = self.client.post(reverse('add_symbol'), {
            'symbol': 'AAPL'
        })

        symbol_created = Symbol.objects.get(symbol='AAPL')

        self.assertEquals(symbol_created.symbol, 'AAPL')
        self.assertEquals(response.status_code, 201)

    def test_remove_article(self):
        response = self.client.post(reverse('remove_article'), {
            'article_id': '500'
        })

        article_deleted = Article.objects.get_or_none(id=500)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(article_deleted, None)

    def test_list_articles(self):
        response = self.client.get(reverse('news'))

        self.assertEquals(response.status_code, 200)
