# Generated by Django 3.1.6 on 2021-02-19 09:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_book_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='number_of_pages',
            new_name='pagesNum',
        ),
    ]
