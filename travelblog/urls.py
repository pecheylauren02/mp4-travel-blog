from . import views
from django.urls import path


urlpatterns = [
    # Because we are using class based views, we need to use as_view()
    path('', views.PostList.as_view(), name='home'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    # First slug above is a path converter,
    # which converts the slug into a text field
    # The second slug is a keyword name
]