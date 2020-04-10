from django.db import models
from core import models as core_models


class Comment(core_models.TimeStampModel):

    comment = models.CharField(max_length=300)
    user = models.ForeignKey(
        "users.User", related_name="comments", on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        "posts.Post", related_name="comments", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.comment
