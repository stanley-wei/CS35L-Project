# Generated by Django 4.2.1 on 2023-05-17 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='images',
            field=models.ImageField(blank=True, upload_to='review_images/'),
        ),
    ]
