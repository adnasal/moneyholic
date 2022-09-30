import logging

from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APIRequestFactory
from unittest_prettify.colorize import (
    colorize,
    GREEN,
)

from newscraper.models import Symbol, Article
from newscraper.test.factories import SymbolFactory, ArticleFactory

factory = APIRequestFactory()

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(levelname)s: %(message)s')


@colorize(color=GREEN)
class TestViews(TestCase):
    symbol = SymbolFactory()
    article = ArticleFactory()
    client = Client()

    def test_list_symbols(self):
        response = self.client.get(reverse('symbols'))
        self.assertEquals(response.status_code, 200)
        """Test Views: List all symbols -> Working"""

    def test_add_symbol(self):
        response = self.client.post(reverse('add_symbol'), {
            'symbol': 'AAPL',
            "symbol_class": "1",
            "is_enabled": "True"
        })

        symbol_created = Symbol.objects.get(symbol='AAPL')

        self.assertEquals(symbol_created.symbol, 'AAPL')
        self.assertEquals(response.status_code, 201)
        """Test Views: Add symbol -> Working"""

    def test_add_symbol_invalid_class(self):
        response = self.client.post(reverse('add_symbol'), {
            'symbol': 'AAPL',
            "symbol_class": "aA",
            "is_enabled": "True"
        })

        self.assertEquals(response.status_code, 400)
        """Test Views: Add symbol with invalid class -> Working"""

    def test_get_article_does_not_exist(self):
        response = self.client.get(reverse('get_article', args=['0']))

        self.assertEquals(response.status_code, 404)
        """Test Views: Get article that does not exist -> Working"""

    def test_update_symbol(self):
        response = self.client.put(reverse('update_symbol', args=[self.symbol.pk]), {
            'symbol': 'INTC',
            "symbol_class": "1",
            "is_enabled": "True"
        })

        self.assertEquals(response.status_code, 202)
        """Test Views: Update symbol -> Working"""

    def test_update_symbol_does_not_exist(self):
        response = self.client.put(reverse('update_symbol', args=['0']), {
            'symbol': 'TWTR',
            "symbol_class": "1",
            "is_enabled": "True"
        })

        self.assertEquals(response.status_code, 404)
        """Test Views: Update symbol that does not exist -> Working"""

    def test_remove_article(self):
        self.client.delete(reverse('remove_article', args=[self.article.pk]))

        article_deleted = Article.objects.get_or_none(id=self.article.pk)

        self.assertEquals(article_deleted, None)
        """Test Views: Remove article -> Working"""

    def test_remove_article_does_not_exist(self):
        response = self.client.delete(reverse('remove_article', args=['0']))

        self.assertEquals(response.status_code, 404)
        """Test Views: Remove article that does not exist -> Working"""

    def test_list_articles(self):
        response = self.client.get(reverse('news'))

        self.assertEquals(response.status_code, 200)
        """Test Views: List all articles -> Working"""

    def test_news_per_symbol(self):
        response = self.client.get(reverse('news') + f'?symbol={self.symbol.symbol}')
        self.assertEqual(response.status_code, 200)
        """Test Views: News per symbol -> Working"""

    def test_news_per_symbol_class(self):
        response = self.client.get(reverse('news') + f'?symbol_class={self.symbol.symbol_class}')
        self.assertEqual(response.status_code, 200)
        """Test Views: News per symbol class -> Working"""

    def test_recent_news(self):
        response = self.client.get(reverse('recent_news'))
        self.assertEqual(response.status_code, 200)
        """Test Views: Recent news -> Working"""

    def test_news_per_search(self):
        response = self.client.get(reverse('news') + '?search=Apple')
        self.assertEqual(response.status_code, 200)
        """Test Views: News per search -> Working"""

    def test_news_per_date(self):
        response = self.client.get(reverse('news') + f'?date=2022-09-10')
        self.assertEqual(response.status_code, 200)
        """Test Views: News per date -> Working"""

    def test_news_per_date_wrong_format(self):
        response = self.client.get(reverse('news') + '?date=2022/09-10')
        self.assertEqual(response.status_code, 400)
        """Test Views: News per date with wrong format -> Working"""

    def test_news_per_date_to(self):
        response = self.client.get(reverse('news') + '?date_to=2022-09-10')
        self.assertEqual(response.status_code, 200)
        """Test Views: News per date to -> Working"""

    def test_news_per_date_from(self):
        response = self.client.get(reverse('news') + '?date_from=2022-09-10')
        self.assertEqual(response.status_code, 200)
        """Test Views: News per date from -> Working"""

    def test_news_enabled_symbols_only(self):
        articles = Article.objects.filter(symbol=self.symbol)

        self.assertEqual(len(articles), 0)
        """Test Views: News only with enabled symbols -> Working"""

    def test_deleted_articles(self):
        response = self.client.get(reverse('deleted_news'))
        self.assertEqual(response.status_code, 200)
        """Test Views: List all deleted articles -> Working"""

    def test_archived_articles(self):
        response = self.client.get(reverse('archived_news'))
        self.assertEqual(response.status_code, 200)
        """Test Views: List all archived articles -> Working"""

    def test_archive_article_does_not_exist(self):
        response = self.client.put(reverse('archive_article', args=['0']))

        self.assertEquals(response.status_code, 404)
        """Test Views: Archive article that does not exist -> Working"""

    def test_delete_article_does_not_exist(self):
        response = self.client.put(reverse('delete_article', args=['0']))

        self.assertEquals(response.status_code, 404)
        """Test Views: Delete article that does not exist -> Working"""

    def test_remove_article_no_auth(self):
        response = self.client.put(reverse('remove_article', args=[self.article.pk]))

        self.assertEquals(response.status_code, 403)
        """Test Views: Remove article unauthenticated -> Working"""

    def test_archived_article(self):
        self.client.post(reverse('archive_article', args=[self.article.pk]))

        article_archived = Article.objects.get_or_none(id=self.article.pk)

        self.assertEquals(article_archived.is_archived, False)
        """Test Views: Archive article -> Working"""

    def test_deleted_article(self):
        self.client.post(reverse('delete_article', args=[self.article.pk]))

        article_deleted = Article.objects.get_or_none(id=self.article.pk)

        self.assertEquals(article_deleted.is_deleted, False)
        """Test Views: Delete article -> Working"""

    def test_remove_symbol_no_auth(self):
        response = self.client.put(reverse('remove_symbol', args=[self.symbol.pk]))

        self.assertEquals(response.status_code, 403)
        """Test Views: Remove symbol unauthenticated -> Working"""
