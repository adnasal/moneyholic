# Generated by Django 3.2.12 on 2022-09-13 12:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Symbol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(default=None, max_length=8)),
                ('symbol_class', models.PositiveSmallIntegerField(choices=[(0, 'Class A shares'), (1, 'Class B shares'), (2, 'Issuer Qualification Exception'), (3, 'New issue of existing stock'), (4, 'Delinquent'), (5, 'Foreign issue'), (6, 'First convertible bond'), (7, 'Second convertible bond'), (8, 'Third convertible bond'), (9, 'Voting share'), (10, 'Non-voting share'), (11, 'Miscellanous'), (12, 'Fourth-class preferred shares'), (13, 'Third-class preferred shares'), (14, 'Second-class preferred shares'), (15, 'First-class preferred shares'), (16, 'In bankruptcy proceedings'), (17, 'Rights'), (18, 'Shares of beneficial interest'), (19, 'With warrants or rights'), (20, 'Units'), (21, 'When issued or distributed'), (22, 'Warrant'), (23, 'Mutual funds'), (24, 'American Depositary Receipt'), (25, 'Miscellanous situations'), (26, 'Over-the-counter bulletin board'), (27, 'Pink sheets stock'), (28, 'Nasdaq Small-cap'), (29, 'Nasdaq National Market')], default=11)),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=250)),
                ('author', models.TextField(max_length=250)),
                ('text', models.CharField(max_length=10000)),
                ('published_at', models.CharField(max_length=250)),
                ('article_link', models.URLField()),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('symbol', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='article_symbol', to='newscraper.symbol')),
            ],
        ),
    ]
