import json

from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError

from movies.models import Movie, Genre, MovieSeries


class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):
        parser.add_argument('--only_movies', action='store_true', help="Add to database only movies with movies "
                                                                       "series. (In case if genres already exists)")

    def handle(self, *args, **options):
        if not options.get('only_movies'):
            with open('movies/data/genres.json', encoding='utf-8') as genres_file:
                genres = json.loads(genres_file.read())
                try:
                    Genre.objects.bulk_create(
                        [Genre(**genre) for genre in genres]
                    )
                except IntegrityError:
                    raise CommandError("Genres already created")
        with open('movies/data/series.json', encoding='utf-8') as series_file, open('movies/data/movies.json',
                                                                                    encoding='utf-8') as movies_file:
            series, movies = json.loads(series_file.read()), json.loads(movies_file.read())
            try:
                MovieSeries.objects.bulk_create(
                    [MovieSeries(**item) for item in series]
                )
                Movie.objects.bulk_create(
                    [Movie(
                        id=movie["id"],
                        title=movie["title"],
                        description=movie["description"],
                        release_year=movie["release_year"],
                        poster_path=movie["poster_path"],
                        mark=0.0,
                        movie_series_id=movie.get("movie_series_id")

                    ) for movie in movies]
                )
                movie_genres = [
                    [Movie.genres.through(
                        movie_id=movie["id"],
                        genre_id=genre)
                        for genre in movie.get("genre_ids")]
                    for movie in movies
                ]
                movie_genres = [item for sublist in movie_genres for item in sublist]
                Movie.genres.through.objects.bulk_create(movie_genres)
            except IntegrityError:
                raise CommandError("Movies with such titles already exist!")
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(movies)} movies and {len(series)}'))
