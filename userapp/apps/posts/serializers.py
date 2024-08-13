from rest_framework import serializers

from .models import Post, Category, Tag


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("id", "title", "content", "category", "tags", "slug", "created_at")
        depth = 1
