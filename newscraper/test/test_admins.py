from django.contrib.admin.options import (
    ModelAdmin,
)
from django.contrib.admin.sites import AdminSite
from django.test import TestCase
from unittest_prettify.colorize import (
    colorize,
    RED,
)

from newscraper.models import Article, Symbol
from newscraper.test.factories import ArticleFactory, SymbolFactory


class MockRequest:
    pass


class MockSuperUser:
    def has_perm(self, perm, obj=None):
        return True


request = MockRequest()
request.user = MockSuperUser()


@colorize(color=RED)
class ModelAdminArticleTests(TestCase):
    article = ArticleFactory()

    def setUp(self):
        self.site = AdminSite()

    def test_modeladmin_str(self):
        ma = ModelAdmin(Article, self.site)
        self.assertEqual(str(ma), "newscraper.ModelAdmin")
        """Test Admins: Admin model -> Working"""

    def test_default_attributes(self):
        ma = ModelAdmin(Article, self.site)
        self.assertEqual(ma.actions, [])
        self.assertEqual(ma.inlines, [])
        """Test Admins: Default attributes -> Working"""

    def test_default_fields(self):
        ma = ModelAdmin(Article, self.site)

        self.assertEqual(
            list(ma.get_fields(request, self.article)),
            ['symbol', 'title', 'text', 'published_at', 'article_link', 'external_id', 'is_archived', 'is_deleted']
        )
        """Test Admins: Default fields -> Working"""

    def test_default_fieldsets(self):
        ma = ModelAdmin(Article, self.site)
        self.assertEqual(
            ma.get_fieldsets(request),
            [
                (None, {
                    'fields': ['symbol', 'title', 'text', 'published_at', 'article_link', 'external_id', 'is_archived',
                               'is_deleted']
                }),
            ]
        ),
        self.assertEqual(
            ma.get_fieldsets(request, self.article),
            [
                (None, {
                    'fields': ['symbol', 'title', 'text', 'published_at', 'article_link', 'external_id', 'is_archived',
                               'is_deleted']
                }),
            ]

        )
        """Test Admins: Default fieldsets -> Working"""


@colorize(color=RED)
class ModelAdminSymbolTests(TestCase):
    symbol = SymbolFactory()

    def setUp(self):
        self.site = AdminSite()

    def test_modeladmin_str(self):
        ma = ModelAdmin(Article, self.site)
        self.assertEqual(str(ma), "newscraper.ModelAdmin")
        """Test Admins: Admin model -> Working"""

    def test_default_attributes(self):
        ma = ModelAdmin(Symbol, self.site)
        self.assertEqual(ma.actions, [])
        self.assertEqual(ma.inlines, [])
        """Test Admins: Default attributes -> Working"""

    def test_default_fields(self):
        ma = ModelAdmin(Symbol, self.site)

        self.assertEqual(
            list(ma.get_fields(request, self.symbol)), ['symbol', 'is_enabled', 'symbol_class']
        )
        """Test Admins: Default fields -> Working"""

    def test_default_fieldsets(self):
        ma = ModelAdmin(Symbol, self.site)
        self.assertEqual(
            ma.get_fieldsets(request),
            [
                (None, {
                    'fields': ['symbol', 'is_enabled', 'symbol_class']
                }),
            ]
        ),
        self.assertEqual(
            ma.get_fieldsets(request, self.symbol),
            [
                (None, {
                    'fields': ['symbol', 'is_enabled', 'symbol_class']
                }),
            ]

        )
        """Test Admins: Default fieldsets -> Working"""
