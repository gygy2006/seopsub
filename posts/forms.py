from django import forms
from django.forms.widgets import CheckboxSelectMultiple
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from . import models


FILTER_SEARCH = [("title", "제목"), ("body", "내용"), ("title_body", "제목+내용")]


class SearchForm(forms.Form):
    f_search = forms.ChoiceField(choices=FILTER_SEARCH)
    search = forms.CharField(widget=forms.TextInput(attrs={"class": "search_input"}))


class CreatePost(forms.ModelForm):
    class Meta:
        model = models.Post

        fields = ["title", "body", "category"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "w-full h-10 border border-teal-300",
                    "placeholder": "제목을입력하세요",
                }
            ),
            "body": forms.CharField(widget=CKEditorUploadingWidget()),
        }

    def __init__(self, *args, **kwargs):
        super(CreatePost, self).__init__(*args, **kwargs)
        self.fields["category"].choices = [("", "Please Choose Category"),] + list(
            self.fields["category"].choices
        )[1:]

    def save(self, *args, **kwargs):
        post = super().save(commit=False)

        return post
