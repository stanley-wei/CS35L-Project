# Generated by Django 4.2.1 on 2023-06-05 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_book_isbn'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='olid',
            field=models.CharField(blank=True, max_length=11),
        ),
    ]
