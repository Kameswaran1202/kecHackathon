# Generated by Django 4.1.2 on 2023-02-10 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_article_forfinal_article_forfirst_article_forsecond_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='isspl',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
