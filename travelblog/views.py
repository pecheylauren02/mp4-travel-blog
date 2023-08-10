from django.shortcuts import render
from django.views import generic
from .models import Post

# Class based view are useful for making views that are reusable, 
# which can inherit from eachother
# Create the view code
# Create a template to render the view
# Connect up our URLS in the url.py file

class PostList(generic.ListView):
    # Based on generic listview model
    model = Post
    # Inside the class we are telling it to use Post as its model
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    # Contents of our post table
    template_name = 'index.html'
    paginate_by = 6
