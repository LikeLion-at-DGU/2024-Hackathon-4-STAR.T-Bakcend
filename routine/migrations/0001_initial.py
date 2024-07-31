import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('celeb', '0001_initial'),
        ('search', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoutineCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Routine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('sub_title', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('image', models.URLField(blank=True, null=True)),
                ('video_url', models.URLField(blank=True, null=True)),
                ('popular', models.IntegerField(default=0)),
                ('create_at', models.DateField(null=True)),
                ('celeb', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='celeb.celeb')),
                ('theme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search.theme')),
                ('category', models.ManyToManyField(to='routine.routinecategory')),
            ],
        ),
    ]
