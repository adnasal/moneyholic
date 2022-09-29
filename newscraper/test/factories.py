import factory
from django.utils import timezone

from newscraper.models import Symbol, Article
from faker import Faker

fake = Faker()


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
    title = fake.name()
    text = fake.text()
    published_at = factory.Faker("date_time", tzinfo=timezone.utc)
    article_link = 'http://articlelink.com'
    external_id = '20103104adad9##'
    is_archived = False
    is_deleted = False
