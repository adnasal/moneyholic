from django.test import TestCase

from newscraper.models import Symbol, Article
from newscraper.test.factories import SymbolFactory, ArticleFactory


class TestSymbol(TestCase):
    symbol = SymbolFactory()

    def test_symbol_creation(self):
        symbol_test = self.symbol
        self.assertTrue(isinstance(symbol_test, Symbol))

    def test_symbol_default_class(self):
        self.assertEqual(self.symbol.symbol_class, str(Symbol.CLASS_M))

    def test_symbol_model_name(self):
        symbol_db = Symbol.objects.all()

        print(len(symbol_db))

    def test_is_enabled_label(self):
        symbol = self.symbol
        field_label = symbol._meta.get_field('is_enabled').verbose_name
        self.assertEqual(field_label, 'is enabled')

    def test_default_is_enabled_true(self):
        symbol = self.symbol
        is_enabled = symbol._meta.get_field('is_enabled')
        self.assertTrue(is_enabled)


class TestArticle(TestCase):
    article = ArticleFactory()

    def test_article_creation(self):
        article_test = self.article
        self.assertTrue(isinstance(article_test, Article))

    def test_article_symbol(self):
        self.assertEqual(self.article.symbol.symbol_class, str(Symbol.CLASS_K))

    def test_article_link(self):
        article_length = len(self.article.article_link)
        self.assertGreater(article_length, 0)

    def test_title_label(self):
        article = self.article
        field_label = article._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_published_at_label(self):
        article = self.article
        field_label = article._meta.get_field('published_at').verbose_name
        self.assertEqual(field_label, 'published at')

    def test_external_id_label(self):
        article = self.article
        field_label = article._meta.get_field('external_id').verbose_name
        self.assertEqual(field_label, 'external id')

    def test_title_max_length(self):
        article = self.article
        max_length = article._meta.get_field('title').max_length
        self.assertEqual(max_length, 250)

    def test_text_max_length(self):
        article = self.article
        max_length = article._meta.get_field('text').max_length
        self.assertEqual(max_length, 10000)
