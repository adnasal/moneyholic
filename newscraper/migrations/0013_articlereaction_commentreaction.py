# Generated by Django 3.2.12 on 2022-10-06 11:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('newscraper', '0012_articlecomment_is_deleted'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentReaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reacted_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('reaction', models.PositiveSmallIntegerField(choices=[(0, 'Reacted with like.'), (1, 'Reacted with dislike.')])),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='comment_reacted', to='newscraper.articlecomment')),
            ],
        ),
        migrations.CreateModel(
            name='ArticleReaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reacted_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('reaction', models.PositiveSmallIntegerField(choices=[(0, 'Reacted with like.'), (1, 'Reacted with dislike.')])),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='article_reacted', to='newscraper.article')),
            ],
        ),
    ]