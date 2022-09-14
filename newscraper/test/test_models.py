from django.test import TestCase
from newscraper.test.factories import SymbolFactory, ArticleFactory
from newscraper.models import Symbol


class TestSymbol(TestCase):

    symbol = SymbolFactory()

    def test_symbol_model(self):

        self.assertEqual(self.symbol.symbol_class, Symbol.CLASS_L)

    def test_symbol_model_name(self):

        symbol_db = Symbol.objects.all()

        print(len(symbol_db))

