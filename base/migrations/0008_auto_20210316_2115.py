# Generated by Django 3.1.6 on 2021-03-16 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_auto_20210309_0951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='image',
            field=models.ImageField(default='/placeholder.img', null=True, upload_to=''),
        ),
    ]
