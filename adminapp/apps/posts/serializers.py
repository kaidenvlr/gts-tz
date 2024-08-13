from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ("id", "title", "content", "author", "category", "tags", "slug", "created_at", "updated_at")
        depth = 1
