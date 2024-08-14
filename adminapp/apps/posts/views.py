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

    def get_queryset(self):
        data = cache.get('adminposts')
        if not data:
            data = Post.objects.all()
            cache.set('adminposts', data)
        return data

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        cache.clear()


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminUserOrReadOnly,)
    serializer_class = PostSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        data = cache.get(f'adminposts-{self.request.query_params.get("slug")}')
        if not data:
            data = Post.objects.get(slug=self.request.query_params.get('slug'))
            cache.set(f'adminposts-{self.request.query_params.get("slug")}', data)
        return data

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)
        cache.clear()

    def perform_destroy(self, instance):
        cache.clear()
        instance.delete()


class PostFilter(views.APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer
    filter_fields = ['tags', 'category']

    def get_queryset(self):
        data = cache.get(f'adminposts-filter-tag-{"_".join(self.request.query_params.get("tags", "no-tag").split(","))}-cat-{self.request.query_params.get("category", "no-cat")}')
        if not data:
            tags = self.request.query_params.get('tags', "").split(',')
            category = self.request.query_params.get('category', None)
            if category and tags != ['']:
                data = Post.objects.filter(category_id=category, tags__id__in=tags).distinct()
            elif category:
                data = Post.objects.filter(category_id=category)
            elif tags != ['']:
                data = Post.objects.filter(tags__id__in=tags).distinct()
            else:
                data = Post.objects.all()
            cache.set(f'adminposts-filter-tag-{"_".join(self.request.query_params.get("tags", "no-tag").split(","))}-cat-{self.request.query_params.get("category", "no-cat")}', data)
        return data

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        result = []
        for post in queryset:
            result.append(post.get_absolute_url())
        return Response(result, status=200)


class PostSearch(views.APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer

    def get_queryset(self):
        data = cache.get(f'adminposts-search-{self.request.query_params.get("title", "no-title")}')
        if not data:
            title_container = self.request.query_params.get('title').lower()
            data = Post.objects.filter(title__icontains=title_container)
            cache.set(f'adminposts-search-{self.request.query_params.get("title", "no-title")}', data)
        return data

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        result = []
        for post in queryset:
            result.append(post.get_absolute_url())
        return Response(result, status=200)


class TagList(generics.ListCreateAPIView):
    permission_classes = (IsAdminUserOrReadOnly,)
    serializer_class = TagSerializer

    def get_queryset(self):
        data = cache.get('admintags')
        if not data:
            data = Tag.objects.all()
            cache.set('admintags', data)
        return data

    def perform_create(self, serializer):
        cache.clear()
        serializer.save()


class TagDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminUserOrReadOnly,)
    serializer_class = TagSerializer

    def get_queryset(self, *args, **kwargs):
        data = cache.get(f'admintags-{self.request.query_params.get("pk")}')
        if not data:
            data = Tag.objects.get(pk=self.request.query_params.get('pk'))
            cache.set(f'admintags-{self.request.query_params.get("pk")}', data)
        return

    def perform_update(self, serializer):
        cache.clear()
        serializer.save()

    def perform_destroy(self, instance):
        cache.clear()
        instance.delete()


class CategoryList(generics.ListCreateAPIView):
    permission_classes = (IsAdminUserOrReadOnly,)
    serializer_class = CategorySerializer

    def get_queryset(self):
        data = cache.get('admincategories')
        if not data:
            data = Category.objects.all()
            cache.set('admincategories', data)
        return data

    def perform_create(self, serializer):
        cache.clear()
        serializer.save()


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminUserOrReadOnly,)
    serializer_class = CategorySerializer

    def get_queryset(self):
        data = cache.get(f'admincategories-{self.request.query_params.get("pk")}')
        if not data:
            data = Category.objects.get(pk=self.request.query_params.get('pk'))
            cache.set(f'admincategories-{self.request.query_params.get("pk")}', data)
        return data

    def perform_update(self, serializer):
        cache.clear()
        serializer.save()

    def perform_destroy(self, instance):
        cache.clear()
        instance.delete()
