from . import views
from django.urls import path


urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    # Because we are using class based views, we need to use as_view()
]