# Generated by Django 5.0.7 on 2024-08-03 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('celeb', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='celeb',
            name='photo',
            field=models.URLField(default='https://cdn.pixabay.com/photo/2020/08/22/12/36/yoga-5508336_1280.png', max_length=500),
        ),
    ]
