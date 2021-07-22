from django.contrib import admin
from . import models

admin.site.register(models.Genre)


class MoviesInline(admin.TabularInline):
    model = models.Movie


@admin.register(models.MovieSeries)
class MovieSeriesAdmin(admin.ModelAdmin):
    inlines = [MoviesInline]
    list_display = ("title",)
    list_filter = ("title",)


@admin.register(models.Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "release_year", "mark", "movie_series")
    list_filter = ("release_year", "mark", "movie_series")
    search_fields = ("title",)
