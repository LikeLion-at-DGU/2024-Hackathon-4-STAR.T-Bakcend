# Generated by Django 5.0.7 on 2024-08-05 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='theme',
            name='image',
            field=models.URLField(blank=True, default='https://cdn.pixabay.com/photo/2020/08/22/12/36/yoga-5508336_1280.png', max_length=500, null=True),
        ),
    ]
