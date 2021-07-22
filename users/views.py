from django.views.generic import CreateView, DetailView
from django.urls import reverse
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.forms import UserCreationForm


class UserProfile(DetailView):
    model = get_user_model()
    context_object_name = "profile"
    template_name = "registration/profile.html"

    def get_object(self, *args, **kwargs):
        try:
            user = super(UserProfile, self).get_object(*args, **kwargs)
        except AttributeError:
            user = self.request.user
        return user


class UserSignUp(CreateView):
    form_class = UserCreationForm
    template_name = "registration/signup.html"

    def form_valid(self, form):
        """
        If form is valid - authenticates registered user
        """
        reg_user = form.save()
        reg_user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password1'])
        login(self.request, reg_user)
        return super().form_valid(form)

    def get_success_url(self):
        """"
        Redirects authenticate user to the profile page
        """
        return reverse("users:profile", kwargs={"pk": self.request.user.pk})
