from django.contrib import admin
from kobe_wave.models import Image, Article, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id_category", "name"]
    search_fields = ["name"]


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ["id_image", "filename", "year", "month", "hexadecimal"]
    search_fields = ["filename", "words"]
    list_filter = ["year", "month"]


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["id_articles", "title", "author", "category", "image"]
    search_fields = ["title", "author"]
    list_filter = ["category"]
