from django.contrib import admin

from newscraper.models import Article, Symbol


@admin.register(Symbol)
class SymbolAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'

    fieldsets = (
        (None, {
            'fields': ['symbol', 'is_enabled']
        }),
        ('Symbol class', {
            'fields': ['symbol_class']
        }),
    )

    list_display = ['symbol', 'is_enabled', 'symbol_class']
    classes = ['wide', 'extrapretty']
    list_filter = ['is_enabled']


# admin.site.register(Symbol, SymbolAdmin)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ['title', 'text', 'published_at']
        }),
        ('Further information', {
            'fields': ['symbol', 'article_link', 'external_id']
        }),
    )

    list_display = ['title', 'published_at', 'symbol']
    date_hierarchy = 'published_at'
    empty_value_display = '-empty-'
    list_filter = ['symbol']

# admin.site.register(Article, ArticleAdmin)
