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