# Generated by Django 3.2.12 on 2022-10-06 14:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('newscraper', '0014_commentreaction_article'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlecomment',
            name='article_commented',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='article_comment', to='newscraper.article'),
        ),
        migrations.AlterField(
            model_name='articlereaction',
            name='article',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='article_reacted', to='newscraper.article'),
        ),
        migrations.AlterField(
            model_name='commentreaction',
            name='comment',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='comment_reacted', to='newscraper.articlecomment'),
        ),
    ]