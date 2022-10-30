from rest_framework import serializers

from .models import Symbol, Article, ArticleComment, ArticleReaction, CommentReaction, Wordcount


class ChoiceField(serializers.ChoiceField):

    def to_representation(self, obj):
        if obj == '' and self.allow_blank:
            return obj
        return self._choices[obj]

    def to_internal_value(self, data):
        if data == '' and self.allow_blank:
            return ''

        for key, val in self._choices.items():
            if val == data:
                return key
        self.fail('invalid_choice', input=data)


class SymbolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symbol
        fields = [
            "symbol",
            "symbol_class",
            "is_enabled",
        ]


class SymbolViewSerializer(serializers.ModelSerializer):
    symbol_class = ChoiceField(choices=Symbol.CLASS_CHOICES)

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
            "text",
            "commented_at",
            "updated_at",
            "is_deleted",
        ]


class ArticleCommentViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleComment
        fields = [
            "comment_writer",
            "text",
            "commented_at",
            "updated_at",
            "is_deleted",
        ]
        depth = 1


class ArticleReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleReaction
        fields = [
            "reacted_at",
            "reaction",
        ]


class ArticleReactionViewSerializer(serializers.ModelSerializer):
    reaction = ChoiceField(choices=ArticleReaction.REACTION_CHOICES)

    class Meta:
        model = ArticleReaction
        fields = [
            "reacted_at",
            "reaction",
        ]
        depth = 1


class CommentReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentReaction
        fields = [
            "reacted_at",
            "reaction",
        ]


class CommentReactionViewSerializer(serializers.ModelSerializer):
    reaction = ChoiceField(choices=CommentReaction.REACTION_CHOICES)

    class Meta:
        model = CommentReaction

        fields = [
            "reacted_at",
            "reaction",
        ]
        depth = 1


class WordcountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wordcount
        fields = [
            "word",
            "count",
            "updated_at",
            "is_keyword"
        ]
