from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from .models import Post, Comment, Tag
from django.db.models import Count

def index(request):
    all_tags = Tag.objects.all()

    selected_tag = request.GET.get('tag')

    post_list = Post.objects.all()

    if selected_tag:
        post_list = post_list.filter(tags__name=selected_tag)

    context = {
        "post_list": post_list,
        "all_tags": all_tags,
        "selected_tag": selected_tag
    }

    return render(request, "forum/index.html", context)

def detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, "forum/detail.html", {"post": post})

def remove_old_tags():
    old_tags = Tag.objects.annotate(post_count=Count('posts')).filter(post_count=0)
    old_tags.delete()

def add_post(request):
    if request.method == 'POST':
        new_post = Post.objects.create(
            title=request.POST['title'],
            content=request.POST['content'],
            author=request.POST['author'],
        )

        tags_input = request.POST.get('tags', '')
        if tags_input:
            tag_names = [tag.strip() for tag in tags_input.split(',')]
            for tag_name in tag_names:
                if tag_name:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    new_post.tags.add(tag)
                    
        remove_old_tags()
        
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

        post.tags.clear()
        tags_input = request.POST.get('tags', '')
        if tags_input:
            tag_names = [tag.strip() for tag in tags_input.split(',')]
            for tag_name in tag_names:
                if tag_name:
                    tag, created = Tag.objects.get_or_create(name = tag_name)
                    post.tags.add(tag)

        remove_old_tags()

        return redirect('detail', post_id=post_id)
    
    existing_tags = ', '.join(post.tags.values_list('name', flat=True))
    
    return render(request, 'forum/edit_post.html', {'post': post, 'existing_tags': existing_tags})

def edit_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id, post_id=post_id)
    
    if request.method == 'POST':
        comment.content = request.POST['content']
        comment.save()
        return redirect('detail', post_id=post_id)
    
    return render(request, 'forum/edit_comment.html', {'comment': comment, 'post_id': post_id})