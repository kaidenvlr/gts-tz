from apps.posts.models import Post
from apps.posts.serializers import PostSerializer
from rest_framework import views
from rest_framework.response import Response


class PostList(views.APIView):
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=True)

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)


class PostFilter(views.APIView):
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=True)
    filter_fields = ['tags', 'category']

    def get(self, request, *args, **kwargs):
        tags = request.query_params.get('tags', "").split(',')
        category = request.query_params.get('category', None)
        if category and tags != ['']:
            queryset = self.queryset.filter(category_id=category, tags__id__in=tags).distinct()
        elif category:
            queryset = self.queryset.filter(category_id=category)
        elif tags != ['']:
            queryset = self.queryset.filter(tags__id__in=tags).distinct()
        else:
            return Response({"detail": "Please provide tags or category."}, status=400)
        result = []
        for post in queryset:
            result.append(post.get_absolute_url())
        return Response(result, status=200)


class SearchPost(views.APIView):
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=True)

    def get(self, request, *args, **kwargs):
        title_container = request.query_params.get('title').lower()
        if not title_container:
            return Response({"title": "This field is required."}, status=400)
        queryset = self.queryset.filter(title__icontains=title_container)
        result = []
        for post in queryset:
            result.append(post.get_absolute_url())
        return Response(result, status=200)
