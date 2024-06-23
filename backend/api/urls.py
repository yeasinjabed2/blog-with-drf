
from django.urls import path
from .views import BlogList, BlogDetail, CreateBlog

urlpatterns = [
    path('blogs/', BlogList.as_view(), name='blog_list'),
    path('blogs/<int:pk>/', BlogDetail.as_view(), name='blog_detail'),
    path('blogs/create', CreateBlog.as_view(), name='create-blog')
]
