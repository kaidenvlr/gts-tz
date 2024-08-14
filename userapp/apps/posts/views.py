from apps.posts.models import Post
from apps.posts.serializers import PostSerializer
from django.core.cache import cache
from rest_framework import views
from rest_framework.response import Response


class PostList(views.APIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        data = cache.get('userposts')
        if not data:
            data = Post.objects.filter(status=True)
            cache.set('userposts', data)
        return data

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class PostDetail(views.APIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        data = cache.get(f'userposts-{self.request.query_params.get("slug")}')
        if not data:
            data = Post.objects.filter(status=True, slug=self.request.query_params.get('slug'))
            cache.set(f'userposts-{self.request.query_params.get("slug")}', data)
        return data

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset)
        return Response(serializer.data)


class PostFilter(views.APIView):
    serializer_class = PostSerializer
    filter_fields = ['tags', 'category']

    def get_queryset(self):
        data = cache.get(
            f'userposts-filter-tag-{"_".join(self.request.query_params.get("tags", "no-tag").split(","))}-cat-{self.request.query_params.get("category", "no-cat")}')
        if not data:
            tags = self.request.query_params.get('tags', "").split(',')
            category = self.request.query_params.get('category', None)
            if category and tags != ['']:
                data = Post.objects.filter(status=True, category_id=category, tags__id__in=tags).distinct()
            elif category:
                data = Post.objects.filter(status=True, category_id=category)
            elif tags != ['']:
                data = Post.objects.filter(status=True, tags__id__in=tags).distinct()
            else:
                data = Post.objects.filter(status=True)
            cache.set(
                f'userposts-filter-tag-{"_".join(self.request.query_params.get("tags", "no-tag").split(","))}-cat-{self.request.query_params.get("category", "no-cat")}',
                data)
        return data

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        result = []
        for post in queryset:
            result.append(post.get_absolute_url())
        return Response(result, status=200)


class SearchPost(views.APIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        data = cache.get(f'userposts-search-{self.request.query_params.get("title", "no-title")}')
        if not data:
            title_container = self.request.query_params.get('title').lower()
            data = Post.objects.filter(status=True, title__icontains=title_container)
            cache.set(f'userposts-search-{self.request.query_params.get("title", "no-title")}', data)
        return data

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        result = []
        for post in queryset:
            result.append(post.get_absolute_url())
        return Response(result, status=200)
