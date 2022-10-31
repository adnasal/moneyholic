import logging
import warnings
from datetime import datetime

from django.core.cache import cache
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APIRequestFactory
from unittest_prettify.colorize import (
    colorize,
    GREEN,
)

from newscraper.models import Symbol, Article, ArticleComment, Wordcount
from newscraper.test.factories import SymbolFactory, ArticleFactory, ArticleCommentFactory

factory = APIRequestFactory()

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(levelname)s: %(message)s')

cache.set_many({
    'example:1:enabled_symbols': Symbol.objects.filter(is_enabled=True),
    'example:1:deleted_articles': Article.objects.filter(is_deleted=True),
    'example:1:archived_articles': Article.objects.filter(is_archived=True),
    'example:1:article_comments': Article.objects.get(pk=1, is_archived=False, is_deleted=False),
    'example:1:article_reactions': Article.objects.get(pk=1, is_archived=False, is_deleted=False),
    'example:1:comment_reactions': ArticleComment.objects.get(pk=1, is_deleted=False),
    'example:1:comments': ArticleComment.objects.all()
})


@colorize(color=GREEN)
class TestViews(TestCase):

    def setUp(self):
        warnings.simplefilter('ignore', category=ImportWarning)
        self.client = Client()
        self.symbol = SymbolFactory.create_symbol(self)
        self.article = ArticleFactory.create_article(self)
        self.comment = ArticleCommentFactory.create_comment(self)

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

    def test_get_article(self):
        response = self.client.get(reverse('get_article') + f'/?pk={self.article.pk}')

        self.assertEquals(response.status_code, 200)
        """Test Views: Get article -> Working"""

    def test_list_articles(self):
        response = self.client.get(reverse('news'))

        self.assertEquals(response.status_code, 200)
        """Test Views: List all articles -> Working"""

    def test_news_per_symbol(self):
        response = self.client.get(reverse('news') + f'/?symbol={self.symbol.symbol}')
        self.assertEqual(response.status_code, 200)
        """Test Views: News per symbol -> Working"""

    def test_news_per_symbol_class(self):
        response = self.client.get(reverse('news') + f'/?symbol_class={self.symbol.symbol_class}')
        self.assertEqual(response.status_code, 200)
        """Test Views: News per symbol class -> Working"""

    def test_news_per_search(self):
        response = self.client.get(reverse('news') + '/?search=Apple')
        self.assertEqual(response.status_code, 200)
        """Test Views: News per search -> Working"""

    def test_news_per_date(self):
        response = self.client.get(reverse('news') + f'/?date=2022-09-10')
        self.assertEqual(response.status_code, 200)
        """Test Views: News per date -> Working"""

    def test_news_per_date_wrong_format(self):
        response = self.client.get(reverse('news') + '/?date=2022/09-10')
        self.assertEqual(response.status_code, 400)
        """Test Views: News per date with wrong format -> Working"""

    def test_news_per_date_to(self):
        response = self.client.get(reverse('news') + '/?date_to=2022-09-10')
        self.assertEqual(response.status_code, 200)
        """Test Views: News per date to -> Working"""

    def test_news_per_date_from(self):
        response = self.client.get(reverse('news') + '/?date_from=2022-09-10')
        self.assertEqual(response.status_code, 200)
        """Test Views: News per date from -> Working"""

    def test_news_enabled_symbols_only(self):
        articles = Article.objects.filter(symbol=self.symbol).count()

        self.assertEqual(articles, 1)
        """Test Views: News only with enabled symbols -> Working"""

    def test_deleted_articles(self):
        response = self.client.get(reverse('deleted_news'))
        self.assertEqual(response.status_code, 200)
        """Test Views: List all deleted articles -> Working"""

    def test_archived_articles(self):
        response = self.client.get(reverse('archived_news'))
        self.assertEqual(response.status_code, 200)
        """Test Views: List all archived articles -> Working"""

    def test_add_comment(self):
        response = self.client.post((reverse('add_comment') + f'/?pk={self.article.pk}'), {
            "comment_writer": "JaBot",
            "text": "Kakav komentar opet."
        })
        logger.info(response)
        self.assertEquals(response.status_code, 200)
        """Test Views: Add comment -> Working"""

    def test_top_15_keywords(self):
        response = self.client.get(reverse('top_keywords'))
        self.assertEqual(response.status_code, 200)
        """Test Views: Top 15 keywords -> Working"""

    def test_wordcounts(self):
        response = self.client.get(reverse('wordcounts'))
        self.assertEqual(response.status_code, 200)
        """Test Views: Wordcounts -> Working"""

    def test_article_most_likes(self):
        response = self.client.get(reverse('top_likes_article'))
        self.assertEqual(response.status_code, 200)
        """Test Views: Article most likes -> Working"""

    def test_article_most_comments(self):
        response = self.client.get(reverse('top_comments_article'))
        self.assertEqual(response.status_code, 200)
        """Test Views: Article most comments -> Working"""

    def test_comments_most_likes(self):
        response = self.client.get(reverse('top_likes_comment'))
        self.assertEqual(response.status_code, 200)
        """Test Views: Comments most likes -> Working"""

    def test_add_article_reaction(self):
        url = reverse('add_reaction') + '?pk=0'
        logger.info(url)
        response = self.client.post(url, {
            "reaction": "1"
        })

        self.assertEquals(response.status_code, 200)
        """Test Views: Add article reaction -> Working"""

    def test_add_comment_reaction(self):
        response = self.client.post((reverse('add_reaction_comment') + f'/?pk={self.comment.pk}'), {
            "reaction": "1"
        })

        self.assertEquals(response.status_code, 200)
        """Test Views: Add comment reaction -> Working"""

    def test_top_keywords_day(self):
        response = self.client.get(reverse('top_keywords') + f'/?day={datetime.now().day}')

        self.assertEquals(response.status_code, 200)
        """Test Views: Top keywords per day -> Working"""

    def test_top_keywords_month(self):
        response = self.client.get(reverse('top_keywords') + f'/?month={datetime.now().month}')

        self.assertEquals(response.status_code, 200)
        """Test Views: Top keywords per month -> Working"""

    def test_top_keywords_year(self):
        response = self.client.get(reverse('top_keywords') + f'/?year={datetime.now().year}')

        self.assertEquals(response.status_code, 200)
        """Test Views: Top keywords per year -> Working"""

    def test_top_keywords_last_week(self):
        response = self.client.get(reverse('top_keywords') + f'/?last_week')

        self.assertEquals(response.status_code, 200)
        """Test Views: Top keywords of last week -> Working"""

    def test_top_keywords_all(self):
        response = self.client.get(reverse('top_keywords') + f'?all')

        self.assertEquals(response.status_code, 200)
        """Test Views: Top keywords of all times -> Working"""
