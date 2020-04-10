from django.shortcuts import render, reverse, redirect
from django.views.generic import FormView, View
from django.contrib import messages
from . import models, forms


class CreateCommentView(FormView):
    form_class = forms.CreateCommentForm

    def form_valid(self, form):
        post_pk = self.kwargs.get("post_pk")
        try:
            form.save(self.request, post_pk)
        except ValueError:
            return redirect(reverse("users:login"))
        return redirect(reverse("posts:detail", kwargs={"pk": post_pk}))
