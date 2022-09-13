from django.conf.urls import url
from .views import SymbolRemoveView, SymbolAddView, SymbolListView, ArticleListView


urlpatterns = [
    url(r'^api/v1/news', ArticleListView.as_view(), name='news'),
    # news per symbol
    # news per class
    url(r'^api/v1/news/add_symbol', SymbolAddView.as_view(), name='add_symbol'),
    url(r'^api/v1/news/remove_symbol', SymbolRemoveView.as_view(), name='remove_symbol'),
    url(r'^api/v1/news/symbols', SymbolListView.as_view(), name='symbols'),
]