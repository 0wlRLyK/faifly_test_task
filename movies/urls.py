from django.urls import path
from .views import MoviesListByGenres

app_name = "movies"
urlpatterns = [
    path("", MoviesListByGenres.as_view(), name="movies_by_genres")
]
