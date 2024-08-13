from django.urls import path

from . import views

urlpatterns = [
    path('posts/', views.PostList.as_view(), name='post-list'),
    path('posts/<int:pk>/', views.PostDetail.as_view(), name='post-detail'),
    path('posts/filter/', views.PostFilter.as_view(), name='post-filter'),
    path('posts/search/', views.SearchPost.as_view(), name='search-post'),
]
