import logging

from django.http import HttpResponse
from rest_framework import pagination
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView, GenericAPIView, ListAPIView, get_object_or_404
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Symbol, Article
from .serializers import ArticleSerializer, SymbolSerializer

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(levelname)s: %(message)s')


class CustomPagination(pagination.PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 12


class SymbolListView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = SymbolSerializer
    pagination_class = CustomPagination

    def get_queryset(self, *args, **kwargs):
        queryset = Symbol.objects.all()

        return queryset


class SymbolRemoveView(GenericAPIView):
    permission_classes = [AllowAny]
    queryset = Symbol.objects.all()

    def post(self):

        to_delete = self.request.data['symbol_id']
        queryset = Symbol.objects.filter(id=to_delete)

        if not queryset:
            return Response({'Failure': 'Symbol already deleted.'}, status.HTTP_200_OK)
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

    def put(self, request, id):
        serializer = SymbolSerializer(instance=get_object_or_404(Symbol, pk=id), data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.validated_data, status.HTTP_200_OK)


class ArticleListView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ArticleSerializer
    pagination_class = CustomPagination

    def get_queryset(self, *args, **kwargs):
        queryset = Article.objects.all().order_by('symbol_id')

        if self.request.query_params.get('symbol_class') is not None:
            symbol_id = Symbol.objects.filter(symbol_class=self.request.query_params.get('symbol_class'))

            print(self.request.query_params.get('symbol_class'))
            for s in symbol_id:
                query_set = queryset.filter(symbol=s)
        elif self.request.query_params.get('symbol') is not None:
            symbol_id = Symbol.objects.get(symbol=self.request.query_params.get('symbol'))

            print(self.request.query_params.get('symbol'))
            query_set = queryset.filter(symbol=symbol_id.id)
        else:
            query_set = queryset.all()

        return query_set


class ArticleView(GenericAPIView):
    permission_classes = [AllowAny]
    queryset = Article.objects.all()

    def get(self, id):
        to_get = self.request.data['article_id']
        response = Article.objects.get_or_none(id=to_get)

        if response is None:
            return HttpResponse('Article does not exist.')
        else:
            return HttpResponse(response, content_type="application/json")


class ArticleRemoveView(GenericAPIView):
    permission_classes = [AllowAny]
    queryset = Article.objects.all()

    def post(self, id):
        to_delete = self.request.data['article_id']
        queryset = Article.objects.filter(id=to_delete)

        if not queryset:
            return Response({'Failure': 'Article already deleted.'}, status.HTTP_200_OK)
        else:
            queryset.delete()

            return Response(
                data={
                    "message": "You have successfully deleted desired article."
                },
                status=status.HTTP_200_OK
            )
