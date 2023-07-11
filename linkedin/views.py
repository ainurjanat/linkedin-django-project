from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import User, Profile, Connection, Post, Comment

@login_required
def home(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    connections = user.connections.all()
    posts = Post.objects.filter(author__in=connections.values('connection')).order_by('-created_at')
    context = {'profile': profile, 'connections': connections, 'posts': posts}
    return render(request, 'home.html', context)

@login_required
def profile (request, username):
    profile_user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=profile_user)
    context = {'profile': profile}
    return render(request, 'profile.html', context)

@login_required
def connect(request, username):
    user = request.user
    profile_user = get_object_or_404(User, username=username)
    connection = Connection(user=user, connection=profile_user)
    connection.save()
    return redirect('profile', username=username)

@login_required
def create_post(request):
    if request.method == 'POST':
        content = request.POST['content']
        post = Post(author=request.user, content=content)
        post.save()
        return redirect('home')
    return render(request, 'create_post.html')

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    context = {'post':post, 'comments': comments}
    return render(request, 'post_detail.html', context)

@login_required
def create_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        content = request.POST['content']
        comment = Comment(post=post, author=request.user, content=content)
        comment.save()
        return redirect('post_detail', post_id=post_id)
    return redirect('home')

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.revome(request.user)
    else:
        post.likes.add(request.user)
    return redirect('post_detail', post_id=post_id)

@login_required
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)
    return redirect('post_detail', post_id=comment.post.id)