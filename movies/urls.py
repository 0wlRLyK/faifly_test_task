from django.urls import path
from .views import MoviesListByGenres, MovieDetails, MoviesListDetails, MoviesListCreate, MoviesListUpdate, \
    AddMovieToList

app_name = "movies"
urlpatterns = [
    path("", MoviesListByGenres.as_view(), name="by_genres"),
    path('movie/<int:pk>/', MovieDetails.as_view(), name='movie_details'),
    path('movies_list/<int:pk>/', MoviesListDetails.as_view(), name='movies_list_details'),
    path('movies_list/create/', MoviesListCreate.as_view(), name='movies_list_create'),
    path('movies_list/<int:pk>/update/', MoviesListUpdate.as_view(), name='movies_list_update'),
    path('add_to_list/movie/<int:pk>/', AddMovieToList.as_view(), name='add_to_list'),
]
