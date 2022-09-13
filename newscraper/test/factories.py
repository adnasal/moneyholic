import factory
from newscraper.models import Symbol, Article
from datetime import date
import faker


class SymbolFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Symbol

    symbol = factory.Sequence(lambda n: f'AAPL{n}')


class ArticleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Article

    symbol = factory.Sequence(lambda n: f'AAPL{n}')
    title = faker.name()
    text = faker.text()
    published_at = factory.fuzzy.FuzzyDate(date(1984, 1, 1))
    article_link = "http://articlelink.com"
