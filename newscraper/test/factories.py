from datetime import datetime

import factory
from faker import Faker

from newscraper.models import Symbol, Article, ArticleComment, ArticleReaction, CommentReaction

fake = Faker()


class SymbolFactory(factory.django.DjangoModelFactory):

    def create_symbol(self):
        symbol = Symbol.objects.create(

            symbol="META",
            symbol_class="1",
            is_enabled="True"

        )
        return symbol


class ArticleFactory(factory.django.DjangoModelFactory):

    def create_article(self):
        article = Article.objects.create(
            symbol=Symbol.objects.first(),
            title=fake.name(),
            text=fake.text(),
            published_at=datetime.now(),
            article_link='http://articlelink.com',
            external_id='20103104adad9##',
            is_archived=False,
            is_deleted=False
        )

        return article


class ArticleCommentFactory(factory.django.DjangoModelFactory):

    def create_comment(self):
        comment = ArticleComment.objects.create(
            comment_writer=fake.name(),
            article_commented=Article.objects.first(),
            text=fake.text(),
            commented_at=datetime.now(),
            updated_at=datetime.now(),
            is_deleted=False
        )
        return comment


class ArticleReactionFactory(factory.django.DjangoModelFactory):

    def create_reaction(self):
        reaction = ArticleReaction.objects.create(
            article=Article.objects.first(),
            reacted_at=datetime.now(),
            reaction=1
        )
        return reaction


class CommentReactionFactory(factory.django.DjangoModelFactory):

    def create_reaction(self):
        reaction = CommentReaction.objects.create(
            comment=ArticleComment.objects.first(),
            reacted_at=datetime.now(),
            reaction=1
        )
        return reaction
