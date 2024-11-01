from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from .models import Post, Comment, Tag

def index(request):
    post_list = Post.objects.all()
    context = {
        "post_list": post_list,
    }
    return render(request, "forum/index.html", context)

def detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, "forum/detail.html", {"post": post})

def add_post(request):
    if request.method == 'POST':
        new_post = Post.objects.create(
            title=request.POST['title'],
            content=request.POST['content'],
            author=request.POST['author'],
        )
        return redirect('detail', post_id=new_post.id)
    return render(request, 'forum/add_post.html')

def add_comment(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_id)
        Comment.objects.create(
            post=post,
            content=request.POST['content'],
            author=request.POST['author']
        )
        return redirect('detail', post_id=post_id)
    
def delete_post(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_id)
        post.delete()
        return redirect('index')
    return HttpResponseForbidden("Invalid method")

def delete_comment(request, post_id, comment_id):
    if request.method == 'POST':
        comment = get_object_or_404(Comment, pk=comment_id, post_id=post_id)
        comment.delete()
        return redirect('detail', post_id=post_id)
    return HttpResponseForbidden("Invalid method")

def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    
    if request.method == 'POST':
        post.title = request.POST['title']
        post.content = request.POST['content']
        post.save()
        return redirect('detail', post_id=post_id)
    
    return render(request, 'forum/edit_post.html', {'post': post})

def edit_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id, post_id=post_id)
    
    if request.method == 'POST':
        comment.content = request.POST['content']
        comment.save()
        return redirect('detail', post_id=post_id)
    
    return render(request, 'forum/edit_comment.html', {'comment': comment, 'post_id': post_id})