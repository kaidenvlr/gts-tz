from django.urls import path

from . import views

urlpatterns = [
    path('posts/', views.PostList.as_view(), name='post_list'),
    path('post/<str:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('posts/filter/', views.PostFilter.as_view(), name='post_filter'),
    path('posts/search/', views.PostSearch.as_view(), name='post_search'),

    path('tags/', views.TagList.as_view(), name='tag_list'),
    path('tags/<int:pk>/', views.TagDetail.as_view(), name='tag_detail'),

    path('categories/', views.CategoryList.as_view(), name='category_list'),
    path('categories/<int:pk>/', views.CategoryDetail.as_view(), name='category_detail'),
]
