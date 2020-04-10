from django.shortcuts import render, reverse, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, DetailView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from . import forms, models
from .mixin import LoggedOutOnlyView


class LoginView(LoggedOutOnlyView, FormView):

    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:list")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            messages.success(self.request, f"Hello {user.first_name}")
            login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        next_arg = self.request.GET.get("next")
        if next_arg is not None:
            return next_arg
        else:
            return reverse("core:list")


class SignUpView(LoggedOutOnlyView, FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:list")

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        first_name = form.cleaned_data.get("frist_name")
        password = form.cleaned_data.get("password")
        user = authenticate(
            self.request, last_name=first_name, username=email, password=password
        )
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


def log_out(request):
    logout(request)
    return redirect(reverse("core:list"))


class UserProfileView(DetailView):
    model = models.User
    template_name = "users/profile.html"
    context_object_name = "user"
