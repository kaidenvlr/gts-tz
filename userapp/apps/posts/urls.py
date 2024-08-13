from django.urls import path

from . import views

urlpatterns = [
    path('posts/', views.PostList.as_view(), name='post-list'),
    path('posts/filter/', views.PostFilter.as_view(), name='post-filter'),
    path('posts/search/', views.SearchPost.as_view(), name='search-post'),
]
