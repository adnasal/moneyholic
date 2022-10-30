from django.contrib import admin

from newscraper.models import Article, Symbol, ArticleComment, ArticleReaction, CommentReaction, Wordcount


@admin.register(Symbol)
class SymbolAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'

    fieldsets = (
        (None, {
            'fields': ['symbol', 'is_enabled']
        }),
        ('Symbol class', {
            'fields': ['symbol_class']
        }),
    )

    list_display = ['symbol', 'is_enabled', 'symbol_class']
    classes = ['wide', 'extrapretty']
    list_filter = ['is_enabled']
    search_fields = ("symbol__startswith",)


# admin.site.register(Symbol, SymbolAdmin)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ['title', 'text', 'published_at']
        }),
        ('Further information', {
            'fields': ['symbol', 'article_link', 'external_id', 'is_archived', 'is_deleted']
        }),
    )

    list_display = ['title', 'published_at', 'symbol', 'is_archived', 'is_deleted', 'comments', 'likes', 'dislikes']

    def comments(self, obj):
        comments = ArticleComment.objects.filter(article_commented=obj).count()

        return comments

    def likes(self, obj):
        likes = ArticleReaction.objects.filter(reaction=0, article=obj).count()

        return likes

    def dislikes(self, obj):
        dislikes = ArticleReaction.objects.filter(reaction=1, article=obj).count()

        return dislikes

    date_hierarchy = 'published_at'
    empty_value_display = '-empty-'
    list_filter = ['symbol', 'is_archived', 'is_deleted']
    search_fields = ("title__startswith",)


# admin.site.register(Article, ArticleAdmin)


@admin.register(ArticleComment)
class ArticleCommentAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ['comment_writer', 'text', 'commented_at']
        }),
        ('Further information', {
            'fields': ['article_commented', 'updated_at']
        }),
    )

    list_display = ['comment_writer', 'commented_at', 'article_commented', 'likes', 'dislikes']

    def likes(self, obj):
        likes = CommentReaction.objects.filter(reaction=0, comment=obj).count()

        return likes

    def dislikes(self, obj):
        dislikes = CommentReaction.objects.filter(reaction=1, comment=obj).count()

        return dislikes

    date_hierarchy = 'commented_at'
    empty_value_display = '-empty-'
    list_filter = ['article_commented', 'comment_writer']
    search_fields = ("article_commented__startswith",)


# admin.site.register(ArticleComment, ArticleCommentAdmin)


@admin.register(ArticleReaction)
class ArticleReactionAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ['article', 'reaction', 'reacted_at']
        }),
    )

    list_display = ['article']
    date_hierarchy = 'reacted_at'
    empty_value_display = '-empty-'
    list_filter = ['article']
    search_fields = ("article__startswith",)


# admin.site.register(ArticleReaction, ArticleReactionAdmin)


@admin.register(CommentReaction)
class CommentReactionAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ['article', 'comment', 'reaction', 'reacted_at']
        }),
    )

    list_display = ['article', 'comment']
    date_hierarchy = 'reacted_at'
    empty_value_display = '-empty-'
    list_filter = ['article', 'comment']
    search_fields = ("article__startswith", "comment__startswith",)


# admin.site.register(CommentReaction, CommentReactionAdmin)


@admin.register(Wordcount)
class WordcountAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ['word', 'count', 'updated_at', 'is_keyword']
        }),
    )

    list_display = ['word', 'count', 'is_keyword']
    date_hierarchy = 'updated_at'
    empty_value_display = '-empty-'
    list_filter = ['word', 'count', 'is_keyword']

# admin.site.register(Wordcount, WordcountAdmin)
