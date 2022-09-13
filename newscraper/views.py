import logging

from rest_framework import status
from rest_framework.generics import (
    CreateAPIView, GenericAPIView, ListAPIView
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Symbol, Article
from .serializers import ArticleSerializer, SymbolSerializer

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s')


class SymbolListView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ArticleSerializer

    def list(self, request):
        serializer = SymbolSerializer(Symbol.objects.all(), many=True)

        return Response(serializer.data, status.HTTP_200_OK)


class SymbolRemoveView(GenericAPIView):
    permission_classes = [AllowAny]

    def post(self):
        to_delete = self.request.data['symbol_id']
        Symbol.objects.filter(id=to_delete).delete()

        return Response(
            data={
                "message": "You have successfully deleted the symbol."
            },
            status=status.HTTP_200_OK
        )


class SymbolAddView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = SymbolSerializer

    def put(self, request):
        serializer = SymbolSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.validated_data, status.HTTP_201_CREATED)


class ArticleListView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ArticleSerializer
    # pagination_class

    def get_queryset(self, *args, **kwargs):
        queryset = Article.objects.all().order_by('symbol_id')

        if self.request.query_params.get('symbol') is not None:
            symbol_id = Symbol.objects.get(symbol=self.request.query_params.get('symbol'))

            print(self.request.query_params.get('symbol'))
            article_list = queryset.filter(symbol=symbol_id.id)
        else:
            article_list = queryset.all()
        return article_list
