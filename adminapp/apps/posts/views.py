from rest_framework import views, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from apps.posts.models import Post
from apps.posts.serializers import PostSerializer


class PostList(generics.ListCreateAPIView):
    permission_classes = (IsAdminUser, )
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminUser, )
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class PostFilter(views.APIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = Post.objects.filter(**request.query_params.dict())
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class SearchPost(views.APIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = Post.objects.filter(title__contains=request.query_params.get('title'))
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
