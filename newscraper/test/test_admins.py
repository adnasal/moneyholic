from django.contrib.admin.options import (
    ModelAdmin,
)
from django.contrib.admin.sites import AdminSite
from django.test import TestCase

from newscraper.models import Article, Symbol
from newscraper.test.factories import ArticleFactory, SymbolFactory


class MockRequest:
    pass


class MockSuperUser:
    def has_perm(self, perm, obj=None):
        return True


request = MockRequest()
request.user = MockSuperUser()


class ModelAdminArticleTests(TestCase):
    article = ArticleFactory()

    def setUp(self):
        self.site = AdminSite()

    def test_modeladmin_str(self):
        ma = ModelAdmin(Article, self.site)
        self.assertEqual(str(ma), "newscraper.ModelAdmin")

    def test_default_attributes(self):
        ma = ModelAdmin(Article, self.site)
        self.assertEqual(ma.actions, [])
        self.assertEqual(ma.inlines, [])

    def test_default_fields(self):
        ma = ModelAdmin(Article, self.site)

        self.assertEqual(
            list(ma.get_fields(request, self.article)),
            ['symbol', 'title', 'text', 'published_at', 'article_link', 'external_id']
        )

    def test_default_fieldsets(self):
        ma = ModelAdmin(Article, self.site)
        self.assertEqual(
            ma.get_fieldsets(request),
            [
                (None, {
                    'fields': ['symbol', 'title', 'text', 'published_at', 'article_link', 'external_id']
                }),
            ]
        ),
        self.assertEqual(
            ma.get_fieldsets(request, self.article),
            [
                (None, {
                    'fields': ['symbol', 'title', 'text', 'published_at', 'article_link', 'external_id']
                }),
            ]

        )


class ModelAdminSymbolTests(TestCase):
    symbol = SymbolFactory()

    def setUp(self):
        self.site = AdminSite()

    def test_modeladmin_str(self):
        ma = ModelAdmin(Article, self.site)
        self.assertEqual(str(ma), "newscraper.ModelAdmin")

    def test_default_attributes(self):
        ma = ModelAdmin(Symbol, self.site)
        self.assertEqual(ma.actions, [])
        self.assertEqual(ma.inlines, [])

    def test_default_fields(self):
        ma = ModelAdmin(Symbol, self.site)

        self.assertEqual(
            list(ma.get_fields(request, self.symbol)), ['symbol', 'is_enabled', 'symbol_class']
        )

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
