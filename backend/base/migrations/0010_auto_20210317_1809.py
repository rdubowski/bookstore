# Generated by Django 3.1.6 on 2021-03-17 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_auto_20210317_0937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.ManyToManyField(blank=True, related_name='book_list', to='base.Author'),
        ),
        migrations.AlterField(
            model_name='book',
            name='genre',
            field=models.ManyToManyField(blank=True, related_name='book_list', to='base.Genre'),
        ),
    ]
