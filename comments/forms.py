from django import forms
from django.shortcuts import redirect, reverse
from posts import models as posts_models
from . import models


class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ("comment",)

        widgets = {
            "comment": forms.Textarea(
                attrs={
                    "class": "comment-write w-full border",
                    "placeholder": "댓글을 입력하세요",
                }
            )
        }

    def save(self, request, post_pk, *args, **kwargs):
        comment = super().save(commit=False)
        post = posts_models.Post.objects.get(pk=post_pk)
        comment.user = request.user
        comment.post = post
        comment.save()
        return comment
