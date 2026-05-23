from rest_framework import serializers
from kobe_wave.models import Article, Image, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id_category", "name"]


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["id_image", "hexadecimal", "year"]


class ArticleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    image = ImageSerializer(read_only=True)

    class Meta:
        model = Article
        fields = ["id_articles", "title", "author", "created_at", "category", "image"]
