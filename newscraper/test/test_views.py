import logging

from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APIRequestFactory

from newscraper.models import Symbol, Article
from newscraper.test.factories import SymbolFactory, ArticleFactory

factory = APIRequestFactory()

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(levelname)s: %(message)s')


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

    def test_add_symbol_with_no_data_fails(self):
        response = self.client.post(reverse('add_symbol'), False)
        self.assertEquals(response.status_code, 400)

    def test_remove_article(self):
        self.client.post(reverse('remove_article', args=['545']))

        article_deleted = Article.objects.get_or_none(id=545)

        self.assertEquals(article_deleted, None)

    def test_remove_article_does_not_exist(self):
        response = self.client.post(reverse('remove_article', args=['0']))

        self.assertEquals(response.status_code, 404)

    def test_get_article(self):
        response = self.client.get(reverse('get_article', args=[self.symbol.pk]))

        self.assertEquals(response.status_code, 200)

    def test_list_articles(self):
        response = self.client.get(reverse('news'))

        self.assertEquals(response.status_code, 200)

    def test_pagination_is_four(self):
        response = self.client.get(reverse('news'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 4)

    def test_news_pagination(self):
        response = self.client.get(reverse('news') + '?page=2')
        self.assertEqual(response.status_code, 200)

    def test_news_per_symbol(self):
        response = self.client.get(reverse('news') + '?symbol=TWTR')
        self.assertEqual(response.status_code, 200)

    def test_news_per_symbol_class(self):
        response = self.client.get(reverse('news') + '?symbol_class=1')
        self.assertEqual(response.status_code, 200)