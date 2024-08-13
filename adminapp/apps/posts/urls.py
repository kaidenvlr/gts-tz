from django.urls import path

from . import views

urlpatterns = [
    path('posts/', views.PostList.as_view(), name='post-list'),
    path('posts/<int:pk>/', views.PostDetail.as_view(), name='post-detail'),
    path('posts/filter/', views.PostFilter.as_view(), name='post-filter'),
    path('posts/search/', views.SearchPost.as_view(), name='search-post'),

    path('tags/', views.TagList.as_view(), name='tag-list'),
    path('tags/<int:pk>/', views.TagDetail.as_view(), name='tag-detail'),

    path('categories/', views.CategoryList.as_view(), name='category-list'),
    path('categories/<int:pk>/', views.CategoryDetail.as_view(), name='category-detail'),
]
