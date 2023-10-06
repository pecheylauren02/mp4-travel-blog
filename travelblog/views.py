from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic, View
from django.http import HttpResponseRedirect
from .models import Post, Comment
from .forms import CommentForm, CommentUpdateForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "index.html"
    paginate_by = 6


class PostDetail(LoginRequiredMixin, View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": False,
                "liked": liked,
                "comment_form": CommentForm()
            },
        )

    def post(self, request, slug, *args, **kwargs):

        queryset = Post.objects.filter(status=1)
        # author = request.user
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
        else:
            comment_form = CommentForm()

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": True,
                "comment_form": comment_form,
                "liked": liked
            },
        )


class PostLike(View):

    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))


@method_decorator(login_required, name='dispatch')
class CommentUpdate(View):
    def get(self, request, comment_id, *args, **kwargs):
        comment = get_object_or_404(Comment, id=comment_id, user=request.user)
        form = CommentUpdateForm(instance=comment)
        return render(request, 'comment_update.html',
                      {'form': form, 'comment': comment})

    def post(self, request, comment_id, *args, **kwargs):
        comment = get_object_or_404(Comment, id=comment_id, user=request.user)
        form = CommentUpdateForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('post_detail',
                                        args=[comment.post.slug]))
        return render(request, 'comment_update.html',
                      {'form': form, 'comment': comment})


@method_decorator(login_required, name='dispatch')
class CommentDelete(View):
    def get(self, request, comment_id, *args, **kwargs):
        comment = get_object_or_404(Comment, id=comment_id, user=request.user)
        return render(request, 'comment_delete.html', {'comment': comment})

    def post(self, request, comment_id, *args, **kwargs):
        comment = get_object_or_404(Comment, id=comment_id, user=request.user)
        post_slug = comment.post.slug
        comment.delete()
        return HttpResponseRedirect(reverse('post_detail', args=[post_slug]))
