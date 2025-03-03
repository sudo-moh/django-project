
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from posts.models import Post  # Import the Post model from the posts app
from django.contrib.auth.models import User

@login_required(login_url='/users/login')
def home(request):
    username = request.user.username if request.user.is_authenticated else None
    return render(request, 'home.html', {'username': str(username).title()})

def about(request):
    return render(request, 'about.html')

@login_required(login_url='/users/login')
def profile(request):
    user_posts = Post.objects.filter(author=request.user)  # Fetch posts by the logged-in user
    return render(request, 'profile.html', {'posts': user_posts})

def user_profile(request, username):
    user = get_object_or_404(User, username=username)  # Fetch user by username
    posts = Post.objects.filter(author=user).order_by('-created_at')  # Get user's posts
    return render(request, 'user_profile.html', {'profile_user': user, 'posts': posts})