import logging

from rest_framework import pagination
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView, GenericAPIView, DestroyAPIView, ListAPIView, get_object_or_404
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Symbol, Article
from .serializers import ArticleSerializer, SymbolSerializer

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(levelname)s: %(message)s')


class CustomPagination(pagination.PageNumberPagination):
    page_size = 4
    page_size_query_param = 'page_size'
    max_page_size = 12


class SymbolListView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = SymbolSerializer
    pagination_class = CustomPagination

    def get_queryset(self, *args, **kwargs):
        queryset = Symbol.objects.filter(is_enabled=True)

        return queryset


class SymbolRemoveView(GenericAPIView):
    permission_classes = [AllowAny]
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
    serializer_class = ArticleSerializer
    pagination_class = CustomPagination

    def get_queryset(self, *args, **kwargs):
        queryset = Article.objects.all().order_by('symbol_id')
        query_set = None

        if self.request.query_params.get('symbol_class') is not None:
            symbol_id = Symbol.objects.filter(symbol_class=self.request.query_params.get('symbol_class'),
                                              is_enabled=True)

            print(self.request.query_params.get('symbol_class'))
            for symbol in symbol_id:
                query_set = queryset.filter(symbol=symbol)
        elif self.request.query_params.get('symbol') is not None:
            symbol_id = Symbol.objects.get(symbol=self.request.query_params.get('symbol'), is_enabled=True)

            print(self.request.query_params.get('symbol'))
            query_set = queryset.filter(symbol=symbol_id)

        else:
            query_set = queryset.all()

        return query_set


class ArticleView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ArticleSerializer

    def get(self, request, pk=None):
        try:
            Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            return Response({'Failure': 'Article does not exist.'}, status.HTTP_404_NOT_FOUND)
        else:
            queryset = Article.objects.get(pk=pk)
            serializer = ArticleSerializer(queryset)
            data = serializer.data

            return Response(data, content_type="application/json")


class ArticleRemoveView(DestroyAPIView):
    permission_classes = [AllowAny]
    queryset = Article.objects.all()

    def delete(self, request, pk=None, **kwargs):
        try:
            Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            return Response({'Failure': 'Article does not exist or has been already removed.'},
                            status.HTTP_404_NOT_FOUND)
        else:
            response = Article.objects.get_or_none(id=pk)
            response.delete()
            return Response(
                data={
                    "message": "You have successfully deleted desired article."
                },
                status=status.HTTP_200_OK
            )
