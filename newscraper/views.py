import logging

from rest_framework import pagination
from rest_framework import status
from django.shortcuts import (get_object_or_404,
                              render,
                              HttpResponseRedirect)
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


class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10


class SymbolListView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = SymbolSerializer
   # pagination_class = StandardResultsSetPagination

    def list(self, request):
        serializer = SymbolSerializer(Symbol.objects.all(), many=True)

        return Response(serializer.data, status.HTTP_200_OK)


class SymbolRemoveView(GenericAPIView):
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination

    def delete(self, request, id):
        get_object_or_404(Symbol, pk=id).delete()

        return Response("Symbol is deleted", status.HTTP_200_OK)
    #def delete(self, request, *args, **kwargs):
     #   instance = self.get_object()
      #  self.perform_destroy(instance)
       # return Response(status=status.HTTP_204_NO_CONTENT)

    #def post(self, id):

        #to_delete = get_object_or_404(Symbol, id=id)
        #to_delete.delete()

       # return Response(
        #    data={
        #        "message": "You have successfully deleted the symbol."
         #   },
        #    status=status.HTTP_200_OK
      #  )


class SymbolAddView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = SymbolSerializer

    def create(self, request):

        queryset = Symbol.objects.all()

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

        if self.request.query_params.get('symbol_class') is not None:
            symbol_id = Symbol.objects.get(symbol_class=self.request.query_params.get('symbol_class'))

            print(self.request.query_params.get('symbol_class'))
            query_set = queryset.filter(symbol=symbol_id.id)
        elif self.request.query_params.get('symbol') is not None:
            symbol_id = Symbol.objects.get(symbol=self.request.query_params.get('symbol'))

            print(self.request.query_params.get('symbol'))
            query_set = queryset.filter(symbol=symbol_id.id)
        else:
            query_set = queryset.all()
        return query_set
