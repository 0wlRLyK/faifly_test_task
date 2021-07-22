from django.db import models
from django.conf import settings


class AbstractBaseFields(models.Model):
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class AbstractUserMovieFields(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL,
                             related_name="%(app_label)s_%(class)s_related",
                             related_query_name="%(app_label)s_%(class)ss")
    movie = models.ForeignKey("Movie", null=True, on_delete=models.SET_NULL,
                              related_name="%(app_label)s_%(class)s_related",
                              related_query_name="%(app_label)s_%(class)ss")

    class Meta:
        abstract = True


class Genre(AbstractBaseFields):
    pass


class MovieSeries(AbstractBaseFields):
    pass


class Movie(AbstractBaseFields):
    release_year = models.PositiveIntegerField()
    mark = models.FloatField(default=0.0)
    genres = models.ManyToManyField(Genre, related_name="movies")
    movie_series = models.ForeignKey(MovieSeries, on_delete=models.CASCADE, blank=True, null=True)
    poster_path = models.URLField(blank=True)


class Comment(AbstractUserMovieFields):
    message = models.TextField()


class Mark(AbstractUserMovieFields):
    mark = models.PositiveSmallIntegerField()


class MoviesList(AbstractBaseFields):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL,
                             related_name="movies_lists")
    movies = models.ManyToManyField(Movie, related_name="+")
    is_public = models.BooleanField(default=True)
