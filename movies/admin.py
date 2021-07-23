from django.contrib import admin

from . import models

admin.site.register(models.Genre)
admin.site.register(models.MoviesList)


@admin.register(models.Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display = ("movie", "user", "mark")
    list_filter = ("mark",)


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("movie", "user", "message")
    search_fields = ("movie", "message")


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
