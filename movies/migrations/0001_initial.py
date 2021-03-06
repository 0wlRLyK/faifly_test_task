# Generated by Django 3.2.5 on 2021-07-20 11:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True)),
                ('description', models.TextField(blank=True)),
                ('release_year', models.PositiveIntegerField()),
                ('mark', models.FloatField(default=0.0)),
                ('genres', models.ManyToManyField(related_name='movies', to='movies.Genre')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MovieSeries',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MoviesList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True)),
                ('description', models.TextField(blank=True)),
                ('is_public', models.BooleanField(default=True)),
                ('movies', models.ManyToManyField(related_name='_movies_movieslist_movies_+', to='movies.Movie')),
                ('user',
                 models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='movies_lists',
                                   to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='movie',
            name='movie_series',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='movies.movieseries'),
        ),
        migrations.CreateModel(
            name='Mark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark', models.PositiveSmallIntegerField()),
                ('movie', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL,
                                            related_name='movies_mark_related', related_query_name='movies_marks',
                                            to='movies.movie')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL,
                                           related_name='movies_mark_related', related_query_name='movies_marks',
                                           to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('movie', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL,
                                            related_name='movies_comment_related', related_query_name='movies_comments',
                                            to='movies.movie')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL,
                                           related_name='movies_comment_related', related_query_name='movies_comments',
                                           to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
