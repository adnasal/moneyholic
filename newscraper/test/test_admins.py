import warnings

from django.contrib.admin.options import (
    ModelAdmin,
)
from django.contrib.admin.sites import AdminSite
from django.test import TestCase
from unittest_prettify.colorize import (
    colorize,
    RED,
)

from newscraper.models import Article, Symbol, ArticleComment, Wordcount
from newscraper.test.factories_meta import ArticleFactory, SymbolFactory, ArticleCommentFactory, WordcountFactory


class MockRequest:
    pass


class MockSuperUser:
    def has_perm(self, perm, obj=None):
        return True


request = MockRequest()
request.user = MockSuperUser()


@colorize(color=RED)
class ModelAdminArticleTests(TestCase):

    def setUp(self):
        self.site = AdminSite()
        warnings.simplefilter('ignore', category=ImportWarning)
        self.article = ArticleFactory()

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
        warnings.simplefilter('ignore', category=ImportWarning)

    def test_modeladmin_str(self):
        ma = ModelAdmin(Symbol, self.site)
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


@colorize(color=RED)
class ModelAdminCommentTests(TestCase):
    comment = ArticleCommentFactory()

    def setUp(self):
        self.site = AdminSite()
        warnings.simplefilter('ignore', category=ImportWarning)

    def test_modeladmin_str(self):
        ma = ModelAdmin(ArticleComment, self.site)
        self.assertEqual(str(ma), "newscraper.ModelAdmin")
        """Test Admins: Admin model -> Working"""

    def test_default_attributes(self):
        ma = ModelAdmin(ArticleComment, self.site)
        self.assertEqual(ma.actions, [])
        self.assertEqual(ma.inlines, [])
        """Test Admins: Default attributes -> Working"""

    def test_default_fields(self):
        ma = ModelAdmin(ArticleComment, self.site)

        self.assertEqual(
            list(ma.get_fields(request, self.comment)), ['comment_writer', 'article_commented', 'text', 'is_deleted']
        )
        """Test Admins: Default fields -> Working"""

    def test_default_fieldsets(self):
        ma = ModelAdmin(ArticleComment, self.site)
        self.assertEqual(
            ma.get_fieldsets(request),
            [
                (None, {
                    'fields': ['comment_writer', 'article_commented', 'text', 'is_deleted']
                }),
            ]
        ),
        self.assertEqual(
            ma.get_fieldsets(request, self.comment),
            [
                (None, {
                    'fields': ['comment_writer', 'article_commented', 'text', 'is_deleted']
                }),
            ]

        )
        """Test Admins: Default fieldsets -> Working"""


@colorize(color=RED)
class WordcountAdminTests(TestCase):
    wordcount = WordcountFactory()

    def setUp(self):
        self.site = AdminSite()
        warnings.simplefilter('ignore', category=ImportWarning)

    def test_modelwordcount_str(self):
        ma = ModelAdmin(Wordcount, self.site)
        self.assertEqual(str(ma), "newscraper.ModelAdmin")
        """Test Admins: Admin model -> Working"""

    def test_default_attributes(self):
        ma = ModelAdmin(Wordcount, self.site)
        self.assertEqual(ma.actions, [])
        self.assertEqual(ma.inlines, [])
        """Test Admins: Default attributes -> Working"""

    def test_default_fields(self):
        ma = ModelAdmin(Wordcount, self.site)

        self.assertEqual(
            list(ma.get_fields(request, self.wordcount)), ['word', 'count', 'is_keyword']
        )
        """Test Admins: Default fields -> Working"""

    def test_default_fieldsets(self):
        ma = ModelAdmin(Wordcount, self.site)
        self.assertEqual(
            ma.get_fieldsets(request),
            [
                (None, {
                    'fields': ['word', 'count', 'is_keyword']
                }),
            ]
        ),
        self.assertEqual(
            ma.get_fieldsets(request, self.wordcount),
            [
                (None, {
                    'fields': ['word', 'count', 'is_keyword']
                }),
            ]

        )
        """Test Admins: Default fieldsets -> Working"""
