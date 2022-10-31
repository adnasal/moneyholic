# Generated by Django 3.2.12 on 2022-10-06 12:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('newscraper', '0013_articlereaction_commentreaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='commentreaction',
            name='article',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='article_comment_reaction', to='newscraper.article'),
        ),
    ]
