from django.shortcuts import render, get_object_or_404
from django.views import generic, View
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


class PostDetail(View):
    
    def get(self, request, slug, *args, **kwargs):
        # Gets the post
        queryset = Post.objects.filter(status=1)
        # Gets the published post with the correct slug
        post = get_object_or_404(queryset, slug=slug)
        # Gets comments from post and filters only those that are approved
        comments = post.comments.filter(approved=True).order_by('created_on')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
    
        # Send all of this to our render method
        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "liked": liked
            }
        )