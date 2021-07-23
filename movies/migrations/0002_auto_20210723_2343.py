# Generated by Django 3.2.5 on 2021-07-23 20:43

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='created_datetime',
            field=models.DateTimeField(auto_created=True, default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='movie',
            name='poster_path',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='movie_series',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='series', to='movies.movieseries'),
        ),
        migrations.AlterField(
            model_name='movieslist',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]