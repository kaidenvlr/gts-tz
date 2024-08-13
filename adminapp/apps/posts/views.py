from apps.posts.models import Post
from apps.posts.serializers import PostSerializer
from rest_framework import views, generics
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response


class PostList(generics.ListCreateAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class PostFilter(views.APIView):
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
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=200)


class SearchPost(views.APIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get(self, request, *args, **kwargs):
        title_container = request.query_params.get('title').lower()
        if not title_container:
            return Response({"title": "This field is required."}, status=400)
        queryset = Post.objects.filter(title__icontains=title_container)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=200)
