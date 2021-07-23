from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from movies.models import MoviesList


@receiver(post_save, sender=User)
def create_default_lists(sender, instance, created, **kwargs):
    if created:
        MoviesList.objects.bulk_create([
            MoviesList(user=instance, title="Запланировано"),
            MoviesList(user=instance, title="Просмотрено"),
            MoviesList(user=instance, title="Брошено"),
        ])
