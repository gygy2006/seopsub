from django.urls import path
from posts import views

app_name = "core"

urlpatterns = [path("", views.PostListView.as_view(), name="list")]
