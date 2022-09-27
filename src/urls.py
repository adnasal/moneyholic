from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import re_path, include, reverse_lazy, path
from django.views.generic.base import RedirectView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.routers import DefaultRouter

from newscraper.views import SymbolRemoveView, SymbolAddView, SymbolListView, ArticleListView, ArticleRemoveView, \
    SymbolUpdateView, ArticleView, ArticleRecentNewsView, DeletedArticlesView, ArchivedArticlesView, ArticleArchiveView, ArticleDeleteView
from src.files.urls import files_router
from src.users.urls import users_router

schema_view = get_schema_view(
    openapi.Info(title="Pastebin API", default_version='v1'),
    public=True,
)

router = DefaultRouter()

router.registry.extend(users_router.registry)
router.registry.extend(files_router.registry)

urlpatterns = [
                  path('', RedirectView.as_view(url=reverse_lazy('admin:index'))),
                  # admin panel
                  path('admin/', admin.site.urls),
                  url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
                  # summernote editor
                  path('summernote/', include('django_summernote.urls')),
                  # api
                  url(r'^api/v1/news', ArticleListView.as_view(), name='news'),
                  url(r'^api/v1/recent', ArticleRecentNewsView.as_view(), name='recent_news'),
                  url(r'^api/v1/deleted', DeletedArticlesView.as_view(), name='deleted_news'),
                  url(r'^api/v1/archived', ArchivedArticlesView.as_view(), name='archived_news'),
                  url('api/v1/is_archived_article/(?P<pk>\d+)/$', ArticleArchiveView.as_view(), name='archive_article'),
                  url('api/v1/is_deleted_article/(?P<pk>\d+)/$', ArticleDeleteView.as_view(), name='delete_article'),
                  url('api/v1/remove_article/(?P<pk>\d+)/$', ArticleRemoveView.as_view(), name='remove_article'),
                  url('api/v1/article/(?P<pk>\d+)/$', ArticleView.as_view(), name='get_article'),
                  url(r'^api/v1/add_symbol', SymbolAddView.as_view(), name='add_symbol'),
                  url('api/v1/remove_symbol/', SymbolRemoveView.as_view(), name='remove_symbol'),
                  url('api/v1/update_symbol/(?P<pk>\d+)/$', SymbolUpdateView.as_view(), name='update_symbol'),
                  url(r'^api/v1/symbols', SymbolListView.as_view(), name='symbols'),
                  # auth
                  path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
                  # swagger docs
                  url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0),
                      name='schema-json'),
                  url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
                  url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
                  url(r'^health/', include('health_check.urls')),
                  # the 'api-root' from django rest-frameworks default router
                  re_path(r'^$', RedirectView.as_view(url=reverse_lazy('api-root'), permanent=False)),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
