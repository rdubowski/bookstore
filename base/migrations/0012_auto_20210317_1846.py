# Generated by Django 3.1.6 on 2021-03-17 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_auto_20210317_1840'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='author',
        ),
        migrations.AddField(
            model_name='book',
            name='author',
            field=models.ManyToManyField(blank=True, related_name='book_list', to='base.Author'),
        ),
        migrations.RemoveField(
            model_name='book',
            name='genre',
        ),
        migrations.AddField(
            model_name='book',
            name='genre',
            field=models.ManyToManyField(blank=True, related_name='book_list', to='base.Genre'),
        ),
    ]
