from rest_framework import views
from rest_framework.response import Response

from apps.posts.models import Post
from apps.posts.serializers import PostSerializer


class PostList(views.APIView):
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=True)

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)


class PostFilter(views.APIView):
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=True)

    def get(self, request, *args, **kwargs):
        queryset = Post.objects.filter(status=True, **request.query_params.dict())
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class SearchPost(views.APIView):
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=True)

    def get(self, request, *args, **kwargs):
        queryset = Post.objects.filter(status=True, title__contains=request.query_params.get('title'))
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
