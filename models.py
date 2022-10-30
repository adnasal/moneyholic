import uuid

from django.core.cache import cache
from django.db import models
from django.db.models import QuerySet, Manager
from django.utils import timezone


class GetOrNoneManager(models.Manager):
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None


class CustomQuerySet(QuerySet):
    def update(self, **kwargs):
        cache.delete('articles_all')
        super(CustomQuerySet, self).update(updated_at=timezone.now(), **kwargs)


class CustomManager(Manager):
    def get_queryset(self):
        return CustomQuerySet(self.model, using=self._db)


class Symbol(models.Model):
    objects = GetOrNoneManager()
    # objects = CustomManager()
    symbol = models.CharField(max_length=8, blank=False, null=False, default=None)
    is_enabled = models.BooleanField(default=True)

    CLASS_A = 0
    CLASS_B = 1
    CLASS_C = 2
    CLASS_D = 3
    CLASS_E = 4
    CLASS_F = 5
    CLASS_G = 6
    CLASS_H = 7
    CLASS_I = 8
    CLASS_J = 9
    CLASS_K = 10
    CLASS_L = 11
    CLASS_M = 12
    CLASS_N = 13
    CLASS_O = 14
    CLASS_P = 15
    CLASS_Q = 16
    CLASS_R = 17
    CLASS_S = 18
    CLASS_T = 19
    CLASS_U = 20
    CLASS_V = 21
    CLASS_W = 22
    CLASS_X = 23
    CLASS_Y = 24
    CLASS_Z = 25
    CLASS_OB = 26
    CLASS_PK = 27
    CLASS_SC = 28
    CLASS_NM = 29

    CLASS_CHOICES = (
        (CLASS_A, 'Class A shares'),
        (CLASS_B, 'Class B shares'),
        (CLASS_C, 'Issuer Qualification Exception'),
        (CLASS_D, 'New issue of existing stock'),
        (CLASS_E, 'Delinquent'),
        (CLASS_F, 'Foreign issue'),
        (CLASS_G, 'First convertible bond'),
        (CLASS_H, 'Second convertible bond'),
        (CLASS_I, 'Third convertible bond'),
        (CLASS_J, 'Voting share'),
        (CLASS_K, 'Non-voting share'),
        (CLASS_L, 'Miscellanous'),
        (CLASS_M, 'Fourth-class preferred shares'),
        (CLASS_N, 'Third-class preferred shares'),
        (CLASS_O, 'Second-class preferred shares'),
        (CLASS_P, 'First-class preferred shares'),
        (CLASS_Q, 'In bankruptcy proceedings'),
        (CLASS_R, 'Rights'),
        (CLASS_S, 'Shares of beneficial interest'),
        (CLASS_T, 'With warrants or rights'),
        (CLASS_U, 'Units'),
        (CLASS_V, 'When issued or distributed'),
        (CLASS_W, 'Warrant'),
        (CLASS_X, 'Mutual funds'),
        (CLASS_Y, 'American Depositary Receipt'),
        (CLASS_Z, 'Miscellanous situations'),
        (CLASS_OB, 'Over-the-counter bulletin board'),
        (CLASS_PK, 'Pink sheets stock'),
        (CLASS_SC, 'Nasdaq Small-cap'),
        (CLASS_NM, 'Nasdaq National Market'),
    )

    symbol_class = models.PositiveSmallIntegerField(
        choices=CLASS_CHOICES,
        default=CLASS_L,
    )


class Article(models.Model):
    objects = GetOrNoneManager()
    # objects = CustomManager()
    symbol = models.ForeignKey(Symbol, related_name='article_symbol', on_delete=models.DO_NOTHING)
    title = models.TextField(max_length=250, blank=False)
    text = models.CharField(max_length=10000, blank=False)
    published_at = models.DateTimeField(max_length=300)
    article_link = models.URLField(blank=False)
    external_id = models.CharField(max_length=50, null=True)
    is_archived = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)


def get_default_article():
    return Article.objects.get_or_create(id=str(uuid.uuid4().fields[-1])[:5],
                                         published_at='2013-03-16T17:41:28+00:00', symbol_id='1', text='Default',
                                         title='Default', external_id='Def123')[0]


def get_default_comment():
    return ArticleComment.objects.get_or_create(id=str(uuid.uuid4().fields[-1])[:5],
                                                commented_at='2013-03-16T17:41:28+00:00',
                                                article_commented=get_default_article(), comment_writer='Default')[0]


class ArticleComment(models.Model):
    objects = GetOrNoneManager()
    # objects = CustomManager()
    comment_writer = models.TextField(max_length=250, blank=False)
    article_commented = models.ForeignKey(Article, related_name='article_comment', on_delete=models.DO_NOTHING,
                                          default=get_default_article)
    text = models.CharField(max_length=10000, blank=False, default="What a lame article!")
    commented_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    is_deleted = models.BooleanField(default=False)


class ArticleReaction(models.Model):
    objects = CustomManager()
    like_reaction = 0
    dislike_reaction = 1
    REACTION_CHOICES = (
        (like_reaction, 'Reacted with like.'),
        (dislike_reaction, 'Reacted with dislike.'),
    )
    article = models.ForeignKey(Article, related_name='article_reacted', on_delete=models.DO_NOTHING,
                                default=get_default_article)
    reacted_at = models.DateTimeField(auto_now_add=True, null=True)
    reaction = models.PositiveSmallIntegerField(
        choices=REACTION_CHOICES
    )


class CommentReaction(models.Model):
    objects = CustomManager()
    like_reaction = 0
    dislike_reaction = 1
    REACTION_CHOICES = (
        (like_reaction, 'Reacted with like.'),
        (dislike_reaction, 'Reacted with dislike.'),
    )
    article = models.ForeignKey(Article, related_name='article_comment_reaction', on_delete=models.DO_NOTHING,
                                default=get_default_article)
    comment = models.ForeignKey(ArticleComment, related_name='comment_reacted', on_delete=models.DO_NOTHING,
                                default=get_default_comment)
    reacted_at = models.DateTimeField(auto_now_add=True, null=True)
    reaction = models.PositiveSmallIntegerField(
        choices=REACTION_CHOICES
    )


class Wordcount(models.Model):
    objects = CustomManager()
    word = models.CharField(max_length=50, blank=False)
    count = models.IntegerField(blank=False)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    is_keyword = models.BooleanField(default=False)
