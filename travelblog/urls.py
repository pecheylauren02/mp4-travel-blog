from . import views
from django.urls import path
from .views import create_blog_post


urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('create/', create_blog_post, name='create_blog_post'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('like/<slug:slug>', views.PostLike.as_view(), name='post_like'),
    path('comment/<int:comment_id>/update/', views.CommentUpdate.as_view(), name='comment_update'),
    path('comment/<int:comment_id>/delete/', views.CommentDelete.as_view(), name='comment_delete'), 
]