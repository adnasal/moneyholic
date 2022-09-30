from django.test import TestCase
from unittest_prettify.colorize import (
    colorize,
    MAGENTA,
)

from newscraper.serializers import ArticleSerializer, SymbolSerializer, ArticleViewSerializer, SymbolViewSerializer
from newscraper.test.factories import ArticleFactory, SymbolFactory


@colorize(color=MAGENTA)
class TestArticleSerializer(TestCase):
    article = ArticleFactory()

    def test_serializer_with_empty_data(self):
        serializer = ArticleSerializer(data={})
        self.assertFalse(serializer.is_valid())
        """Test Serializers: Article serializer -> Working"""


@colorize(color=MAGENTA)
class TestArticleViewSerializer(TestCase):
    article = ArticleFactory()

    def test_serializer_with_empty_data(self):
        serializer = ArticleViewSerializer(data={})
        self.assertFalse(serializer.is_valid())
        """Test Serializers: Article view serializer -> Working"""


@colorize(color=MAGENTA)
class TestSymbolSerializer(TestCase):
    symbol = SymbolFactory()

    def test_serializer_with_empty_data(self):
        serializer = SymbolSerializer(data={})
        self.assertTrue(serializer.is_valid())
        """Test Serializers: Symbol serializer -> Working"""


@colorize(color=MAGENTA)
class TestSymbolViewSerializer(TestCase):
    symbol = SymbolFactory()

    def test_serializer_with_empty_data(self):
        serializer = SymbolViewSerializer(data={})
        self.assertTrue(serializer.is_valid())
        """Test Serializers: Symbol view serializer -> Working"""
