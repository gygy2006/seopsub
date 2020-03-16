from django.db import models
from core import models as core_models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField


class Post(core_models.TimeStampModel):
    title = models.CharField(max_length=100)
    summary = models.CharField(max_length=180, null=True)
    author = models.ForeignKey(User, related_name="post", on_delete=models.CASCADE)
    body = RichTextUploadingField()
