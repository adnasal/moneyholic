from datetime import date

import factory
from factory import fuzzy

from newscraper.models import Symbol, Article


class SymbolFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Symbol

    symbol = 'AATL'
    symbol_class = factory.Sequence(lambda n: f'1{n}')
    is_enabled = False


class ArticleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Article

    symbol = SymbolFactory()
    title = factory.Sequence(lambda n: f'Title{n}')
    text = factory.Sequence(lambda n: f'Hello. NIce to meet you{n}')
    published_at = factory.fuzzy.FuzzyDate(date(1984, 1, 1))
    article_link = 'http://articlelink.com'
