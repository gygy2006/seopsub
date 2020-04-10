from django.contrib import admin
from . import models


@admin.register(models.Like)
class LikeAdmin(admin.ModelAdmin):

    list_display = (
        "__str__",
        "total_like",
    )
    filter_horizontal = ("like_user_set",)


@admin.register(models.Category)
class CategoryInLine(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):

    list_display = ("author", "title", "body", "created")
