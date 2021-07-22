from django.views import generic
from django.views.generic.edit import FormMixin

from .models import Movie, Genre
from .forms import GenreForm


class MoviesListByGenres(FormMixin, generic.ListView):
    form_class = GenreForm
    template_name = "movies/movies_list_by_genres.html"
    context_object_name = "movies"

    def get_queryset(self):
        genres_titles = self.request.GET.getlist("genres", Genre.objects.all().values_list("id", flat=True))
        return Movie.objects.filter(genres__id__in=list(genres_titles)).prefetch_related("genres")
