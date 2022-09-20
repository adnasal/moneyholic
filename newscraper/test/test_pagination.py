from django.core.paginator import (
    Paginator,
)
from django.test import TestCase

from newscraper.models import Article
from newscraper.test.factories import ArticleFactory


class ModelPaginationTests(TestCase):
    articles = list()
    for article in range(10):
        articles.append(ArticleFactory())

        def test_first_page(self):
            paginator = Paginator(Article.objects.order_by('id'), 5)
            p = paginator.page(1)
            self.assertEqual("<Page 1 of 1>", str(p))
            self.assertFalse(p.has_previous())
            self.assertEqual(0, p.start_index())
