from django.test import TestCase
from newscraper.test.factories import SymbolFactory, ArticleFactory
from newscraper.models import Symbol


class TestSymbol(TestCase):

    symbol = SymbolFactory()

    def test_symbol_model(self):

        self.assertEqual(self.symbol.symbol_class, str(Symbol.CLASS_L))

    def test_symbol_model_name(self):

        symbol_db = Symbol.objects.all()

        print(len(symbol_db))


class TestArticle(TestCase):

    article = ArticleFactory()

    def test_article_symbol(self):

        self.assertEqual(self.article.symbol.symbol_class, str(Symbol.CLASS_K))

    def test_article_link(self):

        article_length = len(self.article.article_link)
        self.assertGreater(article_length, 0)
