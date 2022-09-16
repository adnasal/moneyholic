from django.test import TestCase

from newscraper.serializers import ArticleSerializer, SymbolSerializer
from newscraper.test.factories import ArticleFactory, SymbolFactory


class TestArticleSerializer(TestCase):
    article = ArticleFactory()

    def test_serializer_with_empty_data(self):
        serializer = ArticleSerializer(data={})
        self.assertFalse(serializer.is_valid())


class TestSymbolSerializer(TestCase):
    symbol = SymbolFactory()

    def test_serializer_with_empty_data(self):
        serializer = SymbolSerializer(data={})
        self.assertTrue(serializer.is_valid())