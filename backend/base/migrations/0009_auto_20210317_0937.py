# Generated by Django 3.1.6 on 2021-03-17 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_auto_20210316_2115'),
    ]

    operations = [
        migrations.RenameField(
            model_name='author',
            old_name='first_name',
            new_name='full_name',
        ),
        migrations.RemoveField(
            model_name='author',
            name='second_name',
        ),
        migrations.AlterField(
            model_name='book',
            name='image',
            field=models.ImageField(default='/placeholder.png', null=True, upload_to=''),
        ),
    ]
