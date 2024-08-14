from apps.common.permissions import IsAdminUserOrReadOnly
from django.core.cache import cache
from rest_framework import views, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Tag, Post, Category
from .serializers import PostSerializer, TagSerializer, CategorySerializer


class PostList(generics.ListCreateAPIView):
    permission_classes = (IsAdminUserOrReadOnly,)
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get_queryset(self):
        data = cache.get('posts')
        if not data:
            data = Post.objects.all()
            cache.set('posts', data)
        return data

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        cache.clear()


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminUserOrReadOnly,)
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = 'slug'

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)
        cache.clear()

    def perform_destroy(self, instance):
        cache.clear()
        instance.delete()


class PostFilter(views.APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    filter_fields = ['tags', 'category']

    def get(self, request, *args, **kwargs):
        tags = request.query_params.get('tags', "").split(',')
        category = request.query_params.get('category', None)
        if category and tags != ['']:
            queryset = Post.objects.filter(category_id=category, tags__id__in=tags).distinct()
        elif category:
            queryset = Post.objects.filter(category_id=category)
        elif tags != ['']:
            queryset = Post.objects.filter(tags__id__in=tags).distinct()
        else:
            return Response({"detail": "Please provide tags or category."}, status=400)
        result = []
        for post in queryset:
            result.append(post.get_absolute_url())
        return Response(result, status=200)


class PostSearch(views.APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get(self, request, *args, **kwargs):
        title_container = request.query_params.get('title').lower()
        if not title_container:
            return Response({"title": "This field is required."}, status=400)
        queryset = Post.objects.filter(title__icontains=title_container)
        result = []
        for post in queryset:
            result.append(post.get_absolute_url())
        return Response(result, status=200)


class TagList(generics.ListCreateAPIView):
    permission_classes = (IsAdminUserOrReadOnly,)
    serializer_class = TagSerializer
    queryset = Tag.objects.all()

    def perform_create(self, serializer):
        cache.clear()
        serializer.save()


class TagDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminUserOrReadOnly,)
    serializer_class = TagSerializer
    queryset = Tag.objects.all()

    def perform_update(self, serializer):
        cache.clear()
        serializer.save()

    def perform_destroy(self, instance):
        cache.clear()
        instance.delete()


class CategoryList(generics.ListCreateAPIView):
    permission_classes = (IsAdminUserOrReadOnly,)
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def perform_create(self, serializer):
        cache.clear()
        serializer.save()


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminUserOrReadOnly,)
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def perform_update(self, serializer):
        cache.clear()
        serializer.save()

    def perform_destroy(self, instance):
        cache.clear()
        instance.delete()
