from rest_framework import serializers

from .models import Symbol, Article


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
