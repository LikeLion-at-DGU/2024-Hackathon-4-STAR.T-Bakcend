# Generated by Django 5.0.7 on 2024-07-28 15:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routine', '0002_alter_routine_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='routine',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='routine.routinecategory'),
        ),
    ]