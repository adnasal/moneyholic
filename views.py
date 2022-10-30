import calendar
import logging
from datetime import datetime, timedelta
from time import strptime

from django.core.cache import cache
from django.db.models import Q, Count
from rest_framework import pagination
from rest_framework import status, filters, serializers, fields
from rest_framework.generics import (
    CreateAPIView, GenericAPIView, DestroyAPIView, ListAPIView, get_object_or_404
)
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from newscraper.tasks import collect_articles_yahoo
from .models import Symbol, Article, ArticleComment, ArticleReaction, CommentReaction, Wordcount
from .serializers import SymbolSerializer, ArticleViewSerializer, SymbolViewSerializer, ArticleCommentSerializer, \
    ArticleCommentViewSerializer, ArticleReactionSerializer, ArticleReactionViewSerializer, CommentReactionSerializer, \
    CommentReactionViewSerializer, WordcountSerializer
from .tasks import save_keywords

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(levelname)s: %(message)s')

today = datetime.now()


class CustomPagination(pagination.PageNumberPagination):
    page_size = 4
    page_size_query_param = 'page_size'
    max_page_size = 12


class ValidateQueryParams(serializers.Serializer):
    search = fields.RegexField(
        "^[\u0621-\u064A\u0660-\u0669 a-zA-Z0-9]{3,30}$", required=False
    )

    date = fields.DateField(format='%Y-%m-%d', required=False)
    date_from = fields.DateField(format='%Y-%m-%d', required=False)
    date_to = fields.DateField(format='%Y-%m-%d', required=False)
    pk = fields.RegexField("^[\u0621-\u064A\u0660-\u0669 0-9]{3,30}$", required=False)
    day = fields.IntegerField(min_value=1, max_value=30, required=False)
    year = fields.IntegerField(min_value=1990, max_value=today.year, required=False)


class SymbolListView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = SymbolViewSerializer
    ordering = ['-id']
    pagination_class = CustomPagination

    def get_queryset(self, *args, **kwargs):
        symbols = cache.get_or_set('enabled_symbols',
                                   Symbol.objects.filter(is_enabled=True).only('symbol', 'symbol_class'))

        return symbols


class SymbolRemoveView(GenericAPIView):
    permission_classes = [IsAdminUser]
    queryset = Symbol.objects.all()

    def post(self):

        queryset = Symbol.objects.filter(id=self.request.data['symbol_id']).only('symbol')

        if queryset.exists():

            if queryset in {'AAPL', 'TWTR', 'GC=F', 'INTC'}:
                return Response(
                    data={
                        "message": "You cannot delete this symbol."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            queryset.delete()

            return Response(
                data={
                    "message": "You have successfully deleted desired symbol."
                },
                status=status.HTTP_200_OK
            )

        return Response({'Failure': 'Symbol already deleted.'}, status.HTTP_404_NOT_FOUND)


class SymbolAddView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = SymbolSerializer

    def create(self, request, **kwargs):
        queryset = Symbol.objects.filter(symbol=self.request.data['symbol'])

        if queryset.exists():
            return Response({'Failure': 'Symbol already exists.'}, status.HTTP_200_OK)

        serializer = SymbolSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.validated_data, status.HTTP_201_CREATED)


class SymbolUpdateView(APIView):
    permission_classes = [AllowAny]
    serializer_class = SymbolSerializer

    def put(self, request):
        try:
            param = self.request.query_params.get('pk', default=None)
            if param is None:
                return Response('Please add primary key.')
            Symbol.objects.get(pk=param)
        except Symbol.DoesNotExist:
            return Response({'Failure': 'Symbol does not exist.'},
                            status.HTTP_404_NOT_FOUND)

        serializer = SymbolSerializer(instance=get_object_or_404(Symbol, pk=param), data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.validated_data, status.HTTP_202_ACCEPTED)


class ArticleListView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ArticleViewSerializer
    ordering = ['-id']
    pagination_class = CustomPagination
    search_fields = ['title', 'text', 'published_at']
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)

    def get_queryset(self, *args, **kwargs):
        param = self.request.query_params

        query_params = ValidateQueryParams(data=param)
        query_params.is_valid(raise_exception=True)

        queryset = Article.objects.filter(is_archived=False, is_deleted=False).order_by('symbol_id').select_related(
            'symbol').defer('external_id')
        symbols = Symbol.objects.filter(is_enabled=True)
        symbol = symbols.values_list('symbol', flat=True)
        symbol_class = symbols.values_list('symbol_class', flat=True)
        query_set = None

        if param.get('search') is not None:

            search = param.get('search')
            query_set = queryset.filter(Q(title__contains=search) | Q(text__contains=search))

        elif param.get('date_from') is not None and param.get('date_to') is not None:
            date_from = datetime.strptime(param.get('date_from'), '%Y-%m-%d')
            date_to = datetime.strptime(param.get('date_to'), '%Y-%m-%d')
            query_set = queryset.filter(published_at__gte=date_from, published_at__lte=date_to)

        elif param.get('date') is not None:
            date = datetime.strptime(param.get('date'), '%Y-%m-%d')
            query_set = queryset.filter(published_at__contains=date)

        elif param.get('symbol_class') is not None and param.get(
                'symbol_class') in symbol_class:
            symbol_id = Symbol.objects.filter(symbol_class=param.get('symbol_class'))

            print(param.get('symbol_class'))
            for symbol in symbol_id:
                query_set = queryset.filter(symbol=symbol)
        elif param.get('symbol') is not None and param.get('symbol') in symbol:
            symbol_id = Symbol.objects.filter(symbol=param.get('symbol'))

            print(param.get('symbol'))
            for symbol in symbol_id:
                query_set = queryset.filter(symbol=symbol)

        else:
            query_set = queryset

        return query_set


class ArticleView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ArticleViewSerializer

    def get(self, request):
        try:
            param = self.request.query_params.get('pk', default=None)
            if param is None:
                return Response('Please add primary key.')
            article = Article.objects.get(pk=param, is_archived=False, is_deleted=False).defer('external_id')
        except Article.DoesNotExist:
            return Response({'Failure': 'Article does not exist.'}, status.HTTP_404_NOT_FOUND)

        serializer = ArticleViewSerializer(article)
        data = serializer.data

        return Response(data, content_type="application/json")


class ArticleRemoveView(DestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Article.objects.all()

    def delete(self, request, **kwargs):
        try:
            param = self.request.query_params.get('pk', default=None)
            if param is None:
                return Response('Please add primary key.')
            article = Article.objects.get(pk=param, is_deleted=True).defer('external_id')
        except Article.DoesNotExist:
            return Response({'Failure': 'Article does not exist or has been already removed.'},
                            status=status.HTTP_404_NOT_FOUND)
        response = article
        response.delete()
        return Response(
            data={
                "message": "You have successfully deleted desired article."
            },
            status=status.HTTP_200_OK
        )


class ArticleArchiveView(DestroyAPIView):
    permission_classes = [AllowAny]
    queryset = Article.objects.all()

    def put(self, request):
        try:
            param = self.request.query_params.get('pk', default=None)
            if param is None:
                return Response('Please add primary key.')
            article = Article.objects.get(pk=param, is_archived=False, is_deleted=False).defer('external_id')
        except Article.DoesNotExist:
            return Response({'Failure': 'Article does not exist.'},
                            status=status.HTTP_404_NOT_FOUND)
        new_article = article
        new_article.is_archived = True
        new_article.save(update_fields=['is_archived'])

        return Response({f'Article archived: {new_article.is_archived} '}, status=status.HTTP_202_ACCEPTED)


class ArticleDeleteView(DestroyAPIView):
    permission_classes = [AllowAny]
    queryset = Article.objects.all()

    def put(self, request):
        try:
            param = self.request.query_params.get('pk', default=None)
            if param is None:
                return Response('Please add primary key.')
            article = Article.objects.get(pk=param, is_deleted=False).defer('external_id')
        except Article.DoesNotExist:
            return Response({'Failure': 'Article does not exist.'},
                            status.HTTP_404_NOT_FOUND)
        new_article = article
        new_article.is_deleted = True
        new_article.save(update_fields=['is_deleted'])

        return Response({f'Article deleted: {new_article.is_deleted} '}, status=status.HTTP_202_ACCEPTED)


class ArticleRecentNewsView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ArticleViewSerializer
    ordering = ['-id']
    pagination_class = CustomPagination

    today = datetime.now()
    yesterday = today - timedelta(days=1)

    def initial_scrape(self):
        data = Article.objects.filter(published_at__range=[self.yesterday, today]).defer('external_id')
        while not data:
            collect_articles_yahoo()
            data = Article.objects.filter(published_at__range=[self.yesterday, today]).defer('external_id')
            if data:
                break

        return data

    def get_queryset(self, *args, **kwargs):

        queryset = self.initial_scrape().select_related('symbol')

        return queryset


class DeletedArticlesView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ArticleViewSerializer
    ordering = ['-id']
    pagination_class = CustomPagination

    def get_queryset(self, *args, **kwargs):
        deleted_articles = cache.get_or_set('deleted_articles', Article.objects.filter(is_deleted=True).defer('external_id'))
        return deleted_articles


class ArchivedArticlesView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ArticleViewSerializer
    ordering = ['-id']
    pagination_class = CustomPagination

    def get_queryset(self, *args, **kwargs):
        archived_articles = cache.get_or_set('archived_articles', Article.objects.filter(is_archived=True).defer('external_id'))
        return archived_articles


class CommentAddView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ArticleCommentSerializer

    def create(self, request, **kwargs):
        try:
            param = self.request.query_params.get('pk', default=None)
            if param is None:
                return Response('Please add primary key.')
            if param is not None:
                article = Article.objects.get(pk=param, is_deleted=False).defer('external_id')
            else:
                return Response({'Failure': 'Please choose which article you want to comment.'},
                                status.HTTP_400_BAD_REQUEST)
        except Article.DoesNotExist:
            return Response({'Failure': 'Article does not exist.'},
                            status.HTTP_404_NOT_FOUND)
        serializer = ArticleCommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        comment = ArticleComment.objects.last()
        comment.article_commented = article
        comment.save(update_fields=['article_commented'])

        serializer.save()
        data = serializer.data

        return Response(data, content_type="application/json")


class ArticleViewComments(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ArticleCommentViewSerializer
    ordering = ['-id']
    pagination_class = CustomPagination

    def get_queryset(self, *args, **kwargs):
        try:
            param = self.request.query_params.get('pk', default=None)
            if param is None:
                return Response('Please add primary key.')
            comments = ArticleComment.objects.filter(article_commented__id=param, article_commented__is_deleted=False)
            return comments
        except Article.DoesNotExist:
            return Response({'Failure': 'Article does not exist.'}, status.HTTP_404_NOT_FOUND)


class CommentRemoveView(DestroyAPIView):
    permission_classes = [AllowAny]
    queryset = ArticleComment.objects.all()

    def delete(self, request, **kwargs):
        try:
            param = self.request.query_params.get('pk', default=None)
            if param is None:
                return Response('Please add primary key.')
            comment = ArticleComment.objects.get(pk=param, is_deleted=False)
        except ArticleComment.DoesNotExist:
            return Response({'Failure': 'Comment does not exist or has been already removed.'},
                            status=status.HTTP_404_NOT_FOUND)
        new_comment = comment
        new_comment.is_deleted = True
        new_comment.save(update_fields=['is_deleted'])

        return Response({f'Comment deleted: {new_comment.is_deleted} '}, status=status.HTTP_202_ACCEPTED)


class ArticleReactionAddView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ArticleReactionSerializer

    def create(self, request, **kwargs):
        try:
            param = self.request.query_params.get('pk', default=None)
            if param is None:
                return Response('Please add primary key.')

            article = Article.objects.get(pk=param, is_deleted=False).defer('external_id')

        except Article.DoesNotExist:
            return Response({'Failure': 'Article does not exist.'},
                            status.HTTP_200_OK)

        serializer = ArticleReactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        reaction = ArticleReaction.objects.last()
        reaction.article = article
        reaction.save(update_fields=['article'])

        return Response(serializer.data, content_type="application/json")


class ArticleReactionView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ArticleReactionViewSerializer
    pagination_class = CustomPagination

    def get_queryset(self, *args, **kwargs):
        try:
            param = self.request.query_params.get('pk', default=None)
            if param is None:
                return Response('Please add primary key.')
            reactions = ArticleReaction.objects.filter(article__id=param, article__is_archived=False,
                                                       article__is_deleted=False)
            return reactions
        except Article.DoesNotExist:
            return Response({'Failure': 'Article does not exist.'}, status.HTTP_404_NOT_FOUND)


class CommentReactionAddView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = CommentReactionSerializer

    def create(self, request, **kwargs):
        try:
            param = self.request.query_params.get('pk', default=None)
            if param is None:
                return Response('Please add primary key.')
            else:
                return Response({'Failure': 'Please choose which comment you want to react on.'},
                                status.HTTP_400_BAD_REQUEST)
        except ArticleComment.DoesNotExist:
            return Response({'Failure': 'Comment does not exist.'},
                            status.HTTP_404_NOT_FOUND)

        obj = ArticleComment.objects.get(pk=param)
        serializer = CommentReactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        reaction = CommentReaction.objects.last()

        field_object = ArticleComment._meta.get_field('article_commented')
        field_value = field_object.value_from_object(obj)

        reaction.article = Article.objects.get(pk=field_value, is_deleted=False).defer('external_id')
        reaction.comment = obj
        reaction.save(update_fields=['article', 'comment'])

        return Response(serializer.data, content_type="application/json")


class CommentReactionView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = CommentReactionViewSerializer
    pagination_class = CustomPagination

    def get_queryset(self, *args, **kwargs):
        try:
            param = self.request.query_params.get('pk', default=None)
            if param is None:
                return Response('Please add primary key.')
            reactions = CommentReaction.objects.filter(comment__id=param, comment__is_deleted=False)
            return reactions
        except ArticleComment.DoesNotExist:
            return Response({'Failure': 'Comment does not exist.'}, status.HTTP_404_NOT_FOUND)


class WordcountListView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = WordcountSerializer
    pagination_class = CustomPagination

    def get_queryset(self, *args, **kwargs):
        wordcount = Wordcount.objects.all().defer('is_keyword')

        return wordcount


class Top15Keywords(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = WordcountSerializer
    ordering = ['-id']
    pagination_class = CustomPagination

    today = datetime.now()

    def get(self, request):
        param = self.request.query_params
        queryset = Wordcount.objects.all().defer('is_keyword')

        query_params = ValidateQueryParams(data=param)
        query_params.is_valid(raise_exception=True)

        if param.get('last_week') is not None:

            query_set = queryset.filter(updated_at__gte=today - timedelta(days=today.weekday(), weeks=1))

        elif param.get('day') is not None:

            day_final = today - timedelta(days=int(param.get('day')))
            query_set = queryset.filter(updated_at__gte=day_final, updated_at__lte=day_final)

        elif param.get('month') and param.get('year') is not None:

            month = param.get('month')
            months = [calendar.month_name[i] for i in range(1, 12)]
            months_int = list(range(1, 12))

            if len(month) > 2 and month in months:
                month = strptime(month, '%B').tm_mon
            elif len(month) > 2 and month not in months:
                return Response('Please type in month correctly either as number or in Month format.')
            elif len(month) < 2 and month not in months_int:
                return Response('Please enter a valid number.')

            query_set = queryset.filter(updated_at__month=month)

        elif param.get('year') is not None:

            query_set = queryset.filter(updated_at__year=param.get('year'))

        elif param.get('all') is not None:

            query_set = queryset

        else:
            return Response('Please check your parameters.')

        return Response(save_keywords(query_set), content_type="application/json")


class ArticleMostLikes(GenericAPIView):
    permission_classes = [AllowAny]
    ordering = ['-id']
    pagination_class = CustomPagination

    def get(self, *args, **kwargs):
        articles = Article.objects.all().defer('external_id')
        my_dict = {}

        for article in articles:
            my_dict[article.title] = ArticleReaction.objects.filter(reaction=0, article=article).count()

        top_5_articles = sorted(my_dict.items(), key=lambda x: x[1])[:5]
        return Response(top_5_articles, content_type="application/json")


class CommentMostLikes(GenericAPIView):
    permission_classes = [AllowAny]
    ordering = ['-id']
    pagination_class = CustomPagination

    def get(self, *args, **kwargs):
        comments = ArticleComment.objects.all().defer('external_id')
        my_dict = {}

        for comment in comments:
            my_dict[comment.text] = CommentReaction.objects.filter(reaction=0, comment=comment).count()

        top_5_comments = sorted(my_dict.items(), key=lambda x: x[1])[:5]
        return Response(top_5_comments, content_type="application/json")


class ArticleMostComments(GenericAPIView):
    permission_classes = [AllowAny]
    ordering = ['-id']
    pagination_class = CustomPagination

    def get(self, *args, **kwargs):
        my_dict = {}

        comments = ArticleComment.objects.annotate(comment_count=Count('article_commented'))

        for comment in comments:
            my_dict[comment.text] = comment.comment_count

        top_5_most_commented_articles = sorted(my_dict.items(), key=lambda x: x[1])[:5]
        return Response(top_5_most_commented_articles, content_type="application/json")
