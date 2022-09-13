from django.test import TestCase
from newscraper.test.factories import SymbolFactory
from newscraper.models import Symbol


class TestSymbol(TestCase):

    def test_symbol_model(self):

        symbol = SymbolFactory()

        self.assertEqual(symbol.symbol_class, Symbol.CLASS_L)

    def test_symbol_model_name(self):
        symbol = SymbolFactory()
        symbol_db = Symbol.objects.all()

        print(len(symbol_db))

