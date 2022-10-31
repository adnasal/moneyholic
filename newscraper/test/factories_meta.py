import factory
from django.utils import timezone
from faker import Faker

from newscraper.models import Symbol, Article, ArticleComment, Wordcount, ArticleReaction, CommentReaction

fake = Faker()


class SymbolFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Symbol

    symbol = 'AATL'
    symbol_class = '1'
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


class ArticleCommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ArticleComment

    comment_writer = fake.name()
    article_commented = ArticleFactory()
    text = fake.text()
    commented_at = factory.Faker("date_time", tzinfo=timezone.utc)
    updated_at = factory.Faker("date_time", tzinfo=timezone.utc)
    is_deleted = False


class WordcountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Wordcount

    word = fake.name()
    count = fake.random_int()
    updated_at = factory.Faker("date_time", tzinfo=timezone.utc)


class ArticleReactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ArticleReaction

    article = ArticleFactory()
    reacted_at = factory.Faker("date_time", tzinfo=timezone.utc)
    reaction = 1


class CommentReactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CommentReaction

    comment = ArticleCommentFactory()
    reacted_at = factory.Faker("date_time", tzinfo=timezone.utc)
    reaction = 1
