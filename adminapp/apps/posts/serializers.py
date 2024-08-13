from rest_framework import serializers

from .models import Post, Tag, Category


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ("id", "title", "content", "author", "category", "tags", "slug", "created_at", "updated_at")
        read_only_fields = ("slug", "created_at", "updated_at")


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")
