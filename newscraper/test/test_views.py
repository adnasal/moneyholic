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
            'symbol': 'AAPL',
            "symbol_class": "1",
            "is_enabled": "True"
        })

        symbol_created = Symbol.objects.get(symbol='AAPL')

        self.assertEquals(symbol_created.symbol, 'AAPL')
        self.assertEquals(response.status_code, 201)

    def test_add_symbol_invalid_class(self):
        response = self.client.post(reverse('add_symbol'), {
            'symbol': 'AAPL',
            "symbol_class": "aA",
            "is_enabled": "True"
        })

        self.assertEquals(response.status_code, 400)

    def test_get_article_does_not_exist(self):
        response = self.client.get(reverse('get_article', args=['0']))

        self.assertEquals(response.status_code, 404)

    def test_update_symbol(self):
        response = self.client.put(reverse('update_symbol', args=[self.symbol.pk]), {
            'symbol': 'INTC',
            "symbol_class": "1",
            "is_enabled": "True"
        })

        self.assertEquals(response.status_code, 202)

    def test_update_symbol_does_not_exist(self):
        response = self.client.put(reverse('update_symbol', args=['0']), {
            'symbol': 'TWTR',
            "symbol_class": "1",
            "is_enabled": "True"
        })

        self.assertEquals(response.status_code, 404)

    def test_remove_article(self):
        self.client.delete(reverse('remove_article', args=[self.article.pk]))

        article_deleted = Article.objects.get_or_none(id=self.article.pk)

        self.assertEquals(article_deleted, None)

    def test_remove_article_does_not_exist(self):
        response = self.client.delete(reverse('remove_article', args=['0']))

        self.assertEquals(response.status_code, 404)

    def test_list_articles(self):
        response = self.client.get(reverse('news'))

        self.assertEquals(response.status_code, 200)

    def test_pagination_is_four(self):
        response = self.client.get(reverse('news'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 4)

    def test_news_pagination(self):
        response = self.client.get(reverse('news') + '?page=1')
        self.assertEqual(response.status_code, 200)

    def test_recent_news_pagination(self):
        response = self.client.get(reverse('recent_news') + '?page=1')
        self.assertEqual(response.status_code, 200)

    def test_news_per_symbol(self):
        response = self.client.get(reverse('news') + f'?symbol={self.symbol.symbol}')
        self.assertEqual(response.status_code, 200)

    def test_news_per_symbol_class(self):
        response = self.client.get(reverse('news') + f'?symbol_class={self.symbol.symbol_class}')
        self.assertEqual(response.status_code, 200)

    def test_recent_news(self):
        response = self.client.get(reverse('recent_news'))
        self.assertEqual(response.status_code, 200)

    def test_news_per_search(self):
        response = self.client.get(reverse('news') + '?search=Apple')
        self.assertEqual(response.status_code, 200)

    def test_news_per_date(self):
        response = self.client.get(reverse('news') + f'?date=2022-09-10')
        self.assertEqual(response.status_code, 200)

    def test_news_per_date_wrong_format(self):
        response = self.client.get(reverse('news') + '?date=2022/09-10')
        self.assertEqual(response.status_code, 400)

    def test_news_per_date_to(self):
        response = self.client.get(reverse('news') + '?date_to=2022-09-10')
        self.assertEqual(response.status_code, 200)

    def test_news_per_date_from(self):
        response = self.client.get(reverse('news') + '?date_from=2022-09-10')
        self.assertEqual(response.status_code, 200)

    def test_news_enabled_symbols_only(self):
        articles = Article.objects.filter(symbol=self.symbol)

        self.assertEqual(len(articles), 0)

    def test_news_enabled_symbols_news_only_random(self):
        result = ["False"]

        enabled_symbol = Symbol.objects.values_list('id').filter(is_enabled__in=result)

        self.assertEqual(len(enabled_symbol), 0)

    def test_deleted_articles(self):
        response = self.client.get(reverse('deleted_news'))
        self.assertEqual(response.status_code, 200)

    def test_archived_articles(self):
        response = self.client.get(reverse('archived_news'))
        self.assertEqual(response.status_code, 200)

    def test_archive_article_does_not_exist(self):
        response = self.client.put(reverse('archive_article', args=['0']))

        self.assertEquals(response.status_code, 404)

    def test_delete_article_does_not_exist(self):
        response = self.client.put(reverse('delete_article', args=['0']))

        self.assertEquals(response.status_code, 404)

    def test_remove_article_no_auth(self):
        response = self.client.put(reverse('remove_article', args=[self.article.pk]))

        self.assertEquals(response.status_code, 403)

    def test_archived_article(self):
        self.client.post(reverse('archive_article', args=[self.article.pk]))

        article_archived = Article.objects.get_or_none(id=self.article.pk)

        self.assertEquals(article_archived, None)

    def test_deleted_article(self):
        self.client.post(reverse('delete_article', args=[self.article.pk]))

        article_deleted = Article.objects.get_or_none(id=self.article.pk)

        self.assertEquals(article_deleted, None)

    def test_remove_symbol_no_auth(self):
        response = self.client.put(reverse('remove_symbol', args=[self.symbol.pk]))

        self.assertEquals(response.status_code, 403)
