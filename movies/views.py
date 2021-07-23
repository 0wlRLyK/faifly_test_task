from django.views import generic
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.detail import SingleObjectMixin

from .models import Movie, Genre, MoviesList, MovieSeries
from .forms import GenreForm


class MoviesListByGenres(FormMixin, generic.ListView):
    form_class = GenreForm
    template_name = "movies/movies_list_by_genres.html"
    context_object_name = "movies"

    def get_queryset(self):
        genres_titles = self.request.GET.getlist("genres", Genre.objects.all().values_list("id", flat=True))
        return Movie.objects.filter(genres__id__in=list(genres_titles)).prefetch_related("genres").distinct()

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            movies_lists = MoviesList.objects.filter(user_id=self.request.user.id)
            context = super().get_context_data(movies_lists=movies_lists)
            return context
        return super().get_context_data()


class MovieDetails(generic.DetailView):
    queryset = Movie.objects.all().select_related("movie_series")
    template_name = "movies/movie_details.html"
    context_object_name = "movie"

    def get_context_data(self, **kwargs):
        series, movies_lists = [], []
        user = self.request.user
        if self.object.movie_series:
            series = Movie.objects.prefetch_related("genres").filter(
                movie_series_id=self.object.movie_series
            ).exclude(id=self.object.id)
        if user.is_authenticated:
            movies_lists = MoviesList.objects.filter(user_id=user.id).exclude(
                movies__exact=self.object
            )
        context = super().get_context_data(series=series, movies_lists=movies_lists)
        return context


class MoviesListDetails(generic.DetailView):
    queryset = MoviesList.objects.select_related("user").prefetch_related("movies__genres").all()
    template_name = "movies/movies_list/detail.html"
    context_object_name = "movie_list"


class MoviesListCreate(LoginRequiredMixin, generic.CreateView):
    model = MoviesList
    fields = ["title", "description", "is_public"]
    template_name = "movies/form.html"
    extra_context = {"post_url": reverse_lazy("movies:movies_list_create")}

    def get_success_url(self):
        return reverse("users:profile")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MoviesListUpdate(LoginRequiredMixin, generic.UpdateView):
    model = MoviesList
    fields = ["title", "description", "is_public"]
    template_name = "movies/form.html"

    def get_context_data(self, **kwargs):
        post_url = reverse("movies:movies_list_update", args=[self.object.pk])
        context = super().get_context_data(post_url=post_url)
        return context

    def get_success_url(self):
        return reverse("users:profile")

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user_id != self.request.user.id:
            return HttpResponseForbidden()
        return super().get(request, *args, **kwargs)


class AddMovieToList(LoginRequiredMixin, SingleObjectMixin, generic.View):
    model = Movie

    def post(self, request, *args, **kwargs):
        movie_list = MoviesList.objects.filter(id=request.POST.get("select-list"), user_id=request.user.id).first()
        movie = self.get_object()
        if not movie_list or movie_list.movies.filter(id=movie.id).exists():
            return HttpResponseForbidden("The list of movies does not exist or the movie has already been added to "
                                         "this list ")
        movie_list.movies.add(movie)
        return HttpResponseRedirect(reverse("movies:movie_details", args=[movie.id]))
