import warnings

from django.core.cache import cache
from django.core.paginator import (
    Paginator,
)
from django.test import TestCase
from django.urls import reverse
from unittest_prettify.colorize import (
    colorize,
    YELLOW,
)

from newscraper.models import Article, Symbol, ArticleComment, Wordcount
from newscraper.test.factories_meta import ArticleFactory, SymbolFactory, ArticleCommentFactory


@colorize(color=YELLOW)
class ModelPaginationTests(TestCase):

    def setUp(self):
        warnings.simplefilter('ignore', category=ImportWarning)
        self.symbol = SymbolFactory()
        self.article = ArticleFactory()
        self.comment = ArticleCommentFactory()

    def test_first_page(self):
        paginator = Paginator(Article.objects.order_by('id'), 5)
        p = paginator.page(1)
        self.assertFalse(p.has_previous())
        self.assertEqual(1, p.start_index())
        """Test Pagination: First page -> Working"""

    def test_pagination_is_four(self):
        response = self.client.get(reverse('news'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 4)
        """Test: Pagination length -> Working"""

    def test_news_pagination(self):
        response = self.client.get(reverse('news') + '?page=1')
        self.assertEqual(response.status_code, 200)
        """Test Pagination: News -> Working"""

    def test_archived_news_pagination(self):
        response = self.client.get(reverse('archived_news') + '?page=1')
        self.assertEqual(response.status_code, 200)
        """Test Pagination: Archived news -> Working"""

    def test_deleted_news_pagination(self):
        response = self.client.get(reverse('deleted_news') + '?page=1')
        self.assertEqual(response.status_code, 200)
        """Test Pagination: Deleted news -> Working"""
