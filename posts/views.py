import json, requests
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.core import serializers
from django.shortcuts import (
    render,
    redirect,
    reverse,
    HttpResponse,
    Http404,
    get_object_or_404,
)
from django.views.generic import (
    FormView,
    ListView,
    DetailView,
    View,
    TemplateView,
    UpdateView,
)
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from comments import forms as comments_form
from users import models as users_models
from users.mixin import LoggedOnlyView
from . import forms, models


class CreatePostView(FormView):

    """ CreatePostView Discription """

    form_class = forms.CreatePost
    template_name = "posts/post_create.html"

    def form_valid(self, form):
        post = form.save()
        post.author = self.request.user
        post.save()
        form.save_m2m()

        like, created = models.Like.objects.get_or_create(post=post)
        return redirect(reverse("core:list"))


class PostListView(ListView):

    """ PostListView Discription """

    template_name = "posts/post_list.html"
    model = models.Post
    paginate_by = 5
    # paginate_orphans = 3
    allow_empty = True
    ordering = "-created"
    context_object_name = "posts"


class PostDetailView(DetailView):

    """ PostDetail Discription """

    tempalte_name = "posts/post_detail.html"
    model = models.Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get("pk")
        categories = models.Category.objects.all()
        context["categories"] = categories
        context["comment_form"] = comments_form.CreateCommentForm()
        return context


class PostEditView(LoggedOnlyView, UpdateView):
    model = models.Post
    template_name = "posts/post_edit.html"
    fields = (
        "title",
        "body",
        "category",
    )

    def get_object(self, queryset=None):
        post = super().get_object(queryset=queryset)
        if post.author.pk != self.request.user.pk:
            raise Http404()
        return post


def search(request):
    search = request.GET.get("search")
    f_search = request.GET.get("f_search")
    if search:
        form = forms.SearchForm(request.GET)
        if form.is_valid():
            search = form.cleaned_data.get("search")

            filter_args = {}

            if f_search == "title":
                filter_args["title__icontains"] = search

                posts = models.Post.objects.filter(**filter_args).order_by("-created")

            elif f_search == "body":
                filter_args["body__icontains"] = search
                posts = models.Post.objects.filter(**filter_args).order_by("-created")
                print(posts)
            else:
                filter_args["search"] = search
                filter_args_value = filter_args["search"]
                posts = models.Post.objects.filter(
                    body__icontains=filter_args_value
                ).order_by("-created") | models.Post.objects.filter(
                    title__icontains=filter_args_value
                ).order_by(
                    "-created"
                )
            return render(
                request, "posts/post_search.html", {"form": form, "posts": posts}
            )
    else:
        form = forms.SearchForm()
    return render(request, "posts/post_search.html", {"form": form})


@login_required
@require_POST
def post_like(request):
    pk = request.POST.get("pk", None)
    try:
        like = models.Like.objects.get(pk=pk)
    except models.Like.DoesNotExist:
        raise Http404
    if request.user in like.like_user_set.all():
        like.like_user_set.remove(request.user)
        message = "cenceled like"
    else:
        like.like_user_set.add(request.user)
        message = "like"

    context = {
        "like_count": like.total_like,
        "message": message,
        "nickname": request.user.first_name,
    }

    return JsonResponse(context)


class ListCategoryView(View):
    def get(self, *args, **kwargs):
        category = self.kwargs.get("category")
        posts = models.Post.objects.filter(category__name=category)
        return render(self.request, "category/category.html", {"posts": posts})
