import logging
from datetime import datetime, timedelta
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.db.models import Q
from rest_framework import pagination
from rest_framework import status, filters, serializers, fields
from rest_framework.generics import (
    CreateAPIView, GenericAPIView, DestroyAPIView, ListAPIView, get_object_or_404
)
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from newscraper.tasks import collect_articles_yahoo
from .models import Symbol, Article
from .serializers import SymbolSerializer, ArticleViewSerializer, SymbolViewSerializer

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(levelname)s: %(message)s')


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


class SymbolListView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = SymbolViewSerializer
    ordering = ['-id']
    pagination_class = CustomPagination


    def get_queryset(self, *args, **kwargs):
        queryset = Symbol.objects.filter(is_enabled=True)

        return queryset


class SymbolRemoveView(GenericAPIView):
    permission_classes = [IsAdminUser]
    queryset = Symbol.objects.all()


    def post(self):

        to_delete = self.request.data['symbol_id']
        queryset = Symbol.objects.filter(id=to_delete)

        if not queryset:
            return Response({'Failure': 'Symbol already deleted.'}, status.HTTP_404_NOT_FOUND)
        else:
            if queryset in {'AAPL', 'TWTR', 'GC=F', 'INTC'}:
                return Response(
                    data={
                        "message": "You cannot delete this symbol."
                    },
                    status=status.HTTP_200_OK
                )
            else:
                queryset.delete()

                return Response(
                    data={
                        "message": "You have successfully deleted desired symbol."
                    },
                    status=status.HTTP_200_OK
                )


class SymbolAddView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = SymbolSerializer


    def create(self, request, **kwargs):

        to_create = self.request.data['symbol']
        queryset = Symbol.objects.filter(symbol=to_create)

        if not queryset:
            serializer = SymbolSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.validated_data, status.HTTP_201_CREATED)
        else:
            return Response({'Failure': 'Symbol already exists.'}, status.HTTP_200_OK)


class SymbolUpdateView(APIView):
    permission_classes = [AllowAny]
    serializer_class = SymbolSerializer

    def put(self, request, pk):
        try:
            Symbol.objects.get(pk=pk)
        except Symbol.DoesNotExist:
            return Response({'Failure': 'Symbol does not exist.'},
                            status.HTTP_404_NOT_FOUND)
        else:
            serializer = SymbolSerializer(instance=get_object_or_404(Symbol, pk=pk), data=request.data)
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

    # @cache_page(CACHE_TTL)
    def get_queryset(self, *args, **kwargs):
        param = self.request.query_params

        query_params = ValidateQueryParams(data=param)
        query_params.is_valid(raise_exception=True)

        queryset = Article.objects.filter(is_archived=False, is_deleted=False).order_by('symbol_id')
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
            symbol_id = Symbol.objects.get(symbol=param.get('symbol'))

            print(param.get('symbol'))
            query_set = queryset.filter(symbol=symbol_id)

        else:
            query_set = queryset.all()

        return query_set


class ArticleView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ArticleViewSerializer

    # def recently_viewed(request, post_id):
    #    session = None
    #   if not "recently_viewed" in request.session:
    #      request.session["recently_viewed"] = []
    #     request.session["recently_viewed"].append(post_id)
    # else:
    #   if post_id in request.session["recently_viewed"]:
    #      request.session["recently_viewed"].remove(post_id)
    # request.session["recently_viewed"].insert(0, post_id)
    # if len(request.session["recently_viewed"]) > 5:
    #   request.session["recently_viewed"].pop()
    # request.session.modified = True

    def get(self, request, pk=None):
        try:
            Article.objects.get(pk=pk, is_archived=False, is_deleted=False)
        except Article.DoesNotExist:
            return Response({'Failure': 'Article does not exist.'}, status.HTTP_404_NOT_FOUND)
        else:
            # self.recently_viewed(pk)
            # recently_viewed_qs = Article.objects.filter(pk__in=request.session.get("recently_viewed", []))
            # recently_viewed_qs = sorted(recently_viewed_qs, key=lambda x: request.session[x.id])
            article = Article.objects.get(pk=pk, is_archived=False, is_deleted=False)
            serializer = ArticleViewSerializer(article)
            data = serializer.data

            return Response(data, content_type="application/json")


class ArticleRemoveView(DestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Article.objects.all()

    def delete(self, request, pk=None, **kwargs):
        try:
            Article.objects.get(pk=pk, is_deleted=True)
        except Article.DoesNotExist:
            return Response({'Failure': 'Article does not exist or has been already removed.'},
                            status=status.HTTP_404_NOT_FOUND)
        else:
            response = Article.objects.get_or_none(id=pk, is_archived=False, is_deleted=False)
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

    def put(self, request, pk):
        try:
            Article.objects.get(pk=pk, is_archived=False, is_deleted=False)
        except Article.DoesNotExist:
            return Response({'Failure': 'Article does not exist.'},
                            status=status.HTTP_404_NOT_FOUND)
        else:
            article = Article.objects.get(pk=pk, is_archived=False, is_deleted=False)
            article.is_archived = True
            article.save(update_fields=['is_archived'])

        return Response({f'Article archived: {article.is_archived} '}, status=status.HTTP_202_ACCEPTED)


class ArticleDeleteView(DestroyAPIView):
    permission_classes = [AllowAny]
    queryset = Article.objects.all()

    def put(self, request, pk):
        try:
            Article.objects.get(pk=pk, is_deleted=False)
        except Article.DoesNotExist:
            return Response({'Failure': 'Article does not exist.'},
                            status.HTTP_404_NOT_FOUND)
        else:
            article = Article.objects.get(pk=pk, is_deleted=False)
            article.is_deleted = True
            article.save(update_fields=['is_deleted'])

        return Response({f'Article deleted: {article.is_deleted} '}, status=status.HTTP_202_ACCEPTED)


class ArticleRecentNewsView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ArticleViewSerializer
    ordering = ['-id']
    pagination_class = CustomPagination

    today = datetime.now()
    yesterday = today - timedelta(days=1)

    def initial_scrape(self):
        data = Article.objects.filter(published_at__range=[self.yesterday, self.today])
        while not data:
            collect_articles_yahoo()
            data = Article.objects.filter(published_at__range=[self.yesterday, self.today])
            if data:
                break

        return data

    def get_queryset(self, *args, **kwargs):

        queryset = self.initial_scrape()

        return queryset


class DeletedArticlesView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ArticleViewSerializer
    ordering = ['-id']
    pagination_class = CustomPagination

    def get_queryset(self, *args, **kwargs):
        queryset = Article.objects.filter(is_deleted=True)
        return queryset


class ArchivedArticlesView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ArticleViewSerializer
    ordering = ['-id']
    pagination_class = CustomPagination

    def get_queryset(self, *args, **kwargs):
        queryset = Article.objects.filter(is_archived=True)
        return queryset
