from django.contrib.auth import urls as django_urls
from django.urls import path

from .views import UserProfile, UserSignUp

app_name = "users"
urlpatterns = [
                  path("profile/", UserProfile.as_view(), name="profile"),
                  path("profile/<int:pk>/", UserProfile.as_view(), name="profile_by_id"),
                  path("signup/", UserSignUp.as_view(), name="signup"),
              ] + django_urls.urlpatterns
