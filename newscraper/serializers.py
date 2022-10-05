from rest_framework import serializers

from .models import Symbol, Article, ArticleComment


class SymbolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symbol
        fields = [
            "symbol",
            "symbol_class",
            "is_enabled",
        ]


class SymbolViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symbol
        fields = [
            "symbol",
            "symbol_class",
            "is_enabled",
        ]
        depth = 1


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = [
            "symbol",
            "title",
            "text",
            "published_at",
            "article_link",
            "external_id",
            "is_archived",
            "is_deleted",
        ]


class ArticleViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = [
            "symbol",
            "title",
            "text",
            "published_at",
            "article_link",
            "external_id",
            "is_archived",
            "is_deleted",
        ]
        depth = 1


class ArticleCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArticleComment
        fields = [
            "comment_writer",
            "article_commented",
            "text",
            "commented_at",
            "updated_at",
        ]


class ArticleCommentViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleComment
        fields = [
            "comment_writer",
            "text",
            "commented_at",
            "updated_at",
        ]
        depth = 1
