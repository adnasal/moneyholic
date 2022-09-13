from rest_framework import serializers
from .models import Symbol, Article


class SymbolSerializer(serializers.ModelSerializer):

    class Meta:

        model = Symbol
        fields = [
            "symbol",
            "symbol_class",
        ]

        read_only_fields = ("symbol",)


class ArticleSerializer(serializers.ModelSerializer):

    class Meta:

        model = Article
        fields = [
            "symbol",
            "title",
            "author",
            "text",
            "published_at" 
            "article_link",
            "created_at",
            "updated_at",
        ]

        read_only_fields = ("symbol", "title", "author",)

