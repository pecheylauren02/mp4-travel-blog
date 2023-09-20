from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


STATUS = ((0, "Draft"), (1, "Published"))


# Make this model more unique
class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    # Cascade means if one record is deleted, related records will be deleted 
    # too, e.g. if we delete user, their blog posts will be deleted too
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="blog_posts")
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    featured_image = CloudinaryField('image', default='placeholder')
    excerpt = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(User, related_name='blog_likes', blank=True)

    # Helpers
    # Order posts based on created at
    # Minus sign means to use descending order
    class Meta:
        ordering = ['-created_on']

    # Magic method that returns a string of an object, should define it coz 
    # default isnt helpful at all
    def __str__(self):
        return self.title
 
    # Helper method to return the total number of likes on a post
    def number_of_likes(self):
        return self.likes.count()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comments')
    # user = models.ForeignKey(User, on_delete=models.CASCADE) Should I use this?
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    # Put in ascending order because we want this to be a conversation
    class Meta:
        ordering = ['created_on']
    
    def __str__(self):
        return f"Comment {self.body} by {self.name}"
