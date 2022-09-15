from django.core.paginator import (
    InvalidPage, Paginator,
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
            self.assertSequenceEqual(p.object_list, self.articles[:5])
            self.assertTrue(p.has_next())
            self.assertFalse(p.has_previous())
            self.assertTrue(p.has_other_pages())
            self.assertEqual(2, p.next_page_number())
            with self.assertRaises(InvalidPage):
                p.previous_page_number()
            self.assertEqual(1, p.start_index())
            self.assertEqual(5, p.end_index())

        def test_last_page(self):
            paginator = Paginator(Article.objects.order_by('id'), 5)
            p = paginator.page(2)
            self.assertEqual("<Page 2 of 2>", str(p))
            self.assertSequenceEqual(p.object_list, self.articles[5:])
            self.assertFalse(p.has_next())
            self.assertTrue(p.has_previous())
            self.assertTrue(p.has_other_pages())
            with self.assertRaises(InvalidPage):
                p.next_page_number()
            self.assertEqual(1, p.previous_page_number())
            self.assertEqual(6, p.start_index())
            self.assertEqual(9, p.end_index())
