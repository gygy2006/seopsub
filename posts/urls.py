from django.urls import path, include
from . import views

app_name = "posts"

urlpatterns = [
    path("search/", views.search, name="search"),
    path("create/", views.CreatePostView.as_view(), name="create"),
    path("like/", views.post_like, name="like"),
    path("<int:pk>/", views.PostDetailView.as_view(), name="detail"),
    path("<int:pk>/edit", views.PostEditView.as_view(), name="edit"),
    path("<str:category>", views.ListCategoryView.as_view(), name="category"),
]
