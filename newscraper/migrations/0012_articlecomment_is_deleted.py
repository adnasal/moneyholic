# Generated by Django 3.2.12 on 2022-10-05 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newscraper', '0011_articlecomment_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlecomment',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
