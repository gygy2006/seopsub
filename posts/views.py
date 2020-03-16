from django.shortcuts import render, redirect, reverse
from django.views.generic import FormView, ListView, DetailView
from . import forms
from . import models


class CreatePostView(FormView):

    """ CreatePostView Discription """

    form_class = forms.CreatePost
    template_name = "posts/post_create.html"

    def form_valid(self, form):
        post = form.save()
        post.author = self.request.user
        post.save()
        return redirect(reverse("posts:create"))


class PostListView(ListView):

    """ PostListView Discription """

    template_name = "posts/post_list.html"
    model = models.Post
    paginate_by = 10
    paginate_orphans = 3
    allow_empty = True
    ordering = "created"
    context_object_name = "posts"


class PostDetailView(DetailView):

    """ PostDetail Discription """

    tempalte_name = "posts/post_detail.html"
    model = models.Post
