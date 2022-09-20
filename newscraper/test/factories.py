from datetime import date, timezone
from datetime import datetime
import factory
from factory import fuzzy
from factory import Faker

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
    published_at = factory.Faker("date_time", tzinfo=timezone.utc)
    article_link = 'http://articlelink.com'
