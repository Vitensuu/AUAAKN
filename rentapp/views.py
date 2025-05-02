<<<<<<< Updated upstream
from django.shortcuts import render

# Create your views here.
=======

from django.shortcuts import render, redirect
from .models import *
from .form import PostForm
from django.contrib.auth.decorators import login_required
# Create your views here.

def Post_list(request):
    posts = Post.objects.order_by('-time_stamp')
    for post in posts:
        att = PostAttachment.objects.filter(post_id = post.pk)
        post.att = att
    return render(request, 'base.html', {'posts':posts})

def DetailsPage(request, pid):
    post = Post.objects.get(pk = pid)
    images = PostAttachment.objects.filter(post_id = post.pk)
    return render(request, 'post/post_details.html', {'post': post, 'images':images})

@login_required
def Add_post(request):
    if request.method != 'POST':
        form = PostForm()
    else:
        form = PostForm(request.POST)
        att = request.FILES.getlist('images')
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            for img in att:
                PostAttachment.objects.create(post_id = post.pk, file=img)
        return redirect(to='post_details', pid=post.pk)
    return render(request, 'post/newpost.html', {'form': form})
    
@login_required
def Edit_post(request, pid):
    post = Post.objects.get(pk = pid)
    post_att = PostAttachment.objects.filter(post_id = pid)
    if request.method != 'POST':
        form = PostForm(instance = post)
    else:
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            att = request.FILES.getlist('images')
            for image in att:
                PostAttachment.objects.create(
                    post_id = pid, file = image
                )
            chosen = request.POST.getlist('attachments')
            for image_id in chosen:
                PostAttachment.objects.get(pk = int(image_id)).delete()
            post.edited = True
            post.save()
        return redirect(to='post_details', pid=post.pk)
    return render(request, 'post/post_edit.html', {'form': form, 'post_att': post_att})

@login_required
def post_delete(request, pid):
    post = Post.objects.get(pk = pid)
    post.delete()
    return redirect(to='post_list')

>>>>>>> Stashed changes
