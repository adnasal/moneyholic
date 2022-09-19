from django.db import models


class GetOrNoneManager(models.Manager):
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None


class Symbol(models.Model):
    objects = GetOrNoneManager()
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
    symbol = models.ForeignKey(Symbol, related_name='article_symbol', on_delete=models.DO_NOTHING)
    title = models.TextField(max_length=250, blank=False)
    text = models.CharField(max_length=10000, blank=False)
    published_at = models.CharField(max_length=250)
    article_link = models.URLField(blank=False)
    external_id = models.CharField(max_length=50, null=True)
