from bs4 import BeautifulSoup
import requests
from django.template.loader import render_to_string
from django.db import models
from django.shortcuts import reverse
from core import models as core_models
from ckeditor_uploader.fields import RichTextUploadingField


class AbstractItem(core_models.TimeStampModel):
    name = models.CharField(max_length=100)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Category(AbstractItem):
    pass


class Post(core_models.TimeStampModel):

    title = models.CharField(max_length=100)
    summary = models.CharField(max_length=180, null=True)
    author = models.ForeignKey(
        "users.User", related_name="post", on_delete=models.CASCADE
    )
    body = RichTextUploadingField()
    category = models.ForeignKey(
        "Category", related_name="post", on_delete=models.CASCADE
    )

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"pk": self.pk})

    def get_img(self):
        try:
            url = f"http://127.0.0.1:8000/posts/{self.pk}"
            bs_html = BeautifulSoup(self.body, "html.parser")
            img = bs_html.find("img")
            img_src = img.get("src")
        except Exception:
            return None
        return img_src

    class Meta:
        ordering = ("-created",)


class Like(models.Model):
    like_user_set = models.ManyToManyField(
        "users.User", related_name="like", blank=True
    )
    post = models.ForeignKey(
        "posts.Post", related_name="like", blank=True, on_delete=models.CASCADE
    )

    @property
    def total_like(self):
        return self.like_user_set.count()

    def __str__(self):
        return self.post.title
