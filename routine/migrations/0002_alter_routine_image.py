# Generated by Django 5.0.7 on 2024-07-28 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routine', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='routine',
            name='image',
            field=models.URLField(blank=True, null=True),
        ),
    ]