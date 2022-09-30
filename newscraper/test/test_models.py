from django.test import TestCase
from unittest_prettify.colorize import (
    colorize,
    BLUE,
)

from newscraper.models import Symbol, Article
from newscraper.test.factories import SymbolFactory, ArticleFactory


@colorize(color=BLUE)
class TestSymbol(TestCase):
    symbol = SymbolFactory()

    def test_symbol_creation(self):
        symbol_test = self.symbol
        self.assertTrue(isinstance(symbol_test, Symbol))
        """Test Models: Symbol creation -> Working"""
    def test_symbol_default_class(self):
        self.assertEqual(self.symbol.symbol_class, str(Symbol.CLASS_M))
        """Test Models: Symbol class -> Working"""
    def test_symbol_model_name(self):
        symbol_db = Symbol.objects.all()

        print(len(symbol_db))
        """Test Models: Symbol name -> Working"""

    def test_is_enabled_label(self):
        symbol = self.symbol
        field_label = symbol._meta.get_field('is_enabled').verbose_name
        self.assertEqual(field_label, 'is enabled')
        """Test Models: Symbol is enabled -> Working"""

    def test_default_is_enabled_true(self):
        symbol = self.symbol
        is_enabled = symbol._meta.get_field('is_enabled')
        self.assertTrue(is_enabled)
        """Test Models: Symbol is enabled -> Working"""


@colorize(color=BLUE)
class TestArticle(TestCase):
    article = ArticleFactory()

    def test_article_creation(self):
        article_test = self.article
        self.assertTrue(isinstance(article_test, Article))
        """Test Models: Article creation -> Working"""

    def test_article_symbol(self):
        self.assertEqual(self.article.symbol.symbol_class, str(Symbol.CLASS_K))
        """Test Models: Article symbol -> Working"""

    def test_article_link(self):
        article_length = len(self.article.article_link)
        self.assertGreater(article_length, 0)
        """Test Models: Article link -> Working"""

    def test_title_label(self):
        article = self.article
        field_label = article._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')
        """Test Models: Article title -> Working"""

    def test_published_at_label(self):
        article = self.article
        field_label = article._meta.get_field('published_at').verbose_name
        self.assertEqual(field_label, 'published at')
        """Test Models: Article published at -> Working"""

    def test_external_id_label(self):
        article = self.article
        field_label = article._meta.get_field('external_id').verbose_name
        self.assertEqual(field_label, 'external id')
        """Test Models: Article external id -> Working"""

    def test_title_max_length(self):
        article = self.article
        max_length = article._meta.get_field('title').max_length
        self.assertEqual(max_length, 250)
        """Test Models: Article title max length -> Working"""

    def test_text_max_length(self):
        article = self.article
        max_length = article._meta.get_field('text').max_length
        self.assertEqual(max_length, 10000)
        """Test Models: Article text max length -> Working"""

    def test_is_archived_label(self):
        article = self.article
        field_label = article._meta.get_field('is_archived').verbose_name
        self.assertEqual(field_label, 'is archived')
        """Test Models: Article is archived -> Working"""

    def test_default_is_archived_false(self):
        article = self.article
        is_archived = article._meta.get_field('is_archived')
        self.assertTrue(is_archived)
        """Test Models: Article is archived -> Working"""

    def test_is_deleted_label(self):
        article = self.article
        field_label = article._meta.get_field('is_deleted').verbose_name
        self.assertEqual(field_label, 'is deleted')
        """Test Models: Article is deleted -> Working"""

    def test_default_is_deleted_false(self):
        article = self.article
        is_deleted = article._meta.get_field('is_deleted')
        self.assertTrue(is_deleted)
        """Test Models: Article is deleted -> Working"""
