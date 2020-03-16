from django import forms
from .models import Post
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class CreatePost(forms.ModelForm):
    class Meta:
        model = Post

        fields = ["title", "body"]

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "width: 100%",
                    "placeholder": "제목을 입력하세요.",
                }
            ),
            "body": forms.CharField(widget=CKEditorUploadingWidget()),
        }

    def save(self, *args, **kwargs):
        post = super().save(commit=False)
        return post
