# Generated by Django 4.2.7 on 2023-12-11 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_alter_news_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='created',
        ),
        migrations.RemoveField(
            model_name='news',
            name='updated',
        ),
        migrations.AddField(
            model_name='news',
            name='pub_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='news',
            name='rating',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='news',
            name='image',
            field=models.ImageField(blank=True, upload_to='images/'),
        ),
    ]
