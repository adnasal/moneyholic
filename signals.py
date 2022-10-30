from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from newscraper.models import Article, ArticleComment, ArticleReaction, CommentReaction, Wordcount, Symbol


@receiver(post_delete, sender=Article, dispatch_uid='archived_article_deleted')
def object_post_delete_handler(sender, **kwargs):
    if cache in 'archived_articles':
        cache.delete('archived_articles')


@receiver(post_delete, sender=Article, dispatch_uid='archived_article_removed')
def object_post_delete_handler(sender, **kwargs):
    if cache in 'archived_articles':
        cache.delete('archived_articles')


@receiver(post_delete, sender=Article, dispatch_uid='deleted_article_removed')
def object_post_delete_handler(sender, **kwargs):
    if cache in 'deleted_articles':
        cache.delete('deleted_articles')


@receiver(post_delete, sender=ArticleComment, dispatch_uid='comment_deleted')
def object_post_delete_handler(sender, **kwargs):
    if cache in 'archived_articles':
        cache.delete('articles')
    elif cache in 'comment_reactions':
        cache.delete('comment_reactions')
    elif cache in 'article_comments':
        cache.delete('article_comments')
    elif cache in 'comments':
        cache.delete('comments')


@receiver(post_save, sender=ArticleComment, dispatch_uid='comment_added')
def object_post_save_handler(sender, **kwargs):
    if cache in 'comment_reactions':
        cache.delete('comment_reactions')
    elif cache in 'article_comments':
        cache.delete('article_comments')
    elif cache in 'comments':
        cache.delete('comments')


@receiver(post_save, sender=Symbol, dispatch_uid='symbol_made')
def object_post_save_handler(sender, **kwargs):
    if cache in 'enabled_symbols':
        cache.delete('enabled_symbols')


@receiver(post_delete, sender=Symbol, dispatch_uid='symbol_deleted')
def object_post_delete_handler(sender, **kwargs):
    if cache in 'enabled_symbols':
        cache.delete('enabled_symbols')


@receiver(post_save, sender=ArticleReaction, dispatch_uid='reaction_added')
def object_post_save_handler(sender, **kwargs):
    if cache in 'article_reactions':
        cache.delete('article_reactions')


@receiver(post_delete, sender=ArticleReaction, dispatch_uid='reaction_deleted')
def object_post_delete_handler(sender, **kwargs):
    if cache in 'article_reactions':
        cache.delete('article_reactions')


@receiver(post_save, sender=CommentReaction, dispatch_uid='comment_reaction_added')
def object_post_save_handler(sender, **kwargs):
    if cache in 'comment_reactions':
        cache.delete('comment_reactions')
    elif cache in 'article_comments':
        cache.delete('article_comments')
    elif cache in 'comments':
        cache.delete('comments')


@receiver(post_delete, sender=CommentReaction, dispatch_uid='comment_reaction_deleted')
def object_post_delete_handler(sender, **kwargs):
    if cache in 'comment_reactions':
        cache.delete('comment_reactions')
    elif cache in 'article_comments':
        cache.delete('article_comments')
    elif cache in 'comments':
        cache.delete('comments')


# done automatically by tasks


@receiver(post_save, sender=Article, dispatch_uid='article_added')
def object_post_save_handler(sender, **kwargs):
    if cache in 'comment_reactions':
        cache.delete('comment_reactions')
    elif cache in 'article_comments':
        cache.delete('article_comments')
    elif cache in 'comments':
        cache.delete('comments')


@receiver(post_save, sender=Wordcount, dispatch_uid='keyword_added')
def object_post_save_handler(sender, **kwargs):
    if cache in 'top_keywords':
        cache.delete('top_keywords')
