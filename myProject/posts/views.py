from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.contrib.auth.decorators import login_required
from . import f
from django.http import JsonResponse


def posts_list(request):
    query = request.GET.get('q', '')
    posts = Post.objects.all()
    
    if query:
        posts = posts.filter(title__icontains=query)  # Search in title (you can extend this)
    
    return render(request, 'posts.html', {'posts': posts, 'query': query})



def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()  # Fetch all comments related to this post

    if request.method == "POST":
        form = f.CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user  # Assign the logged-in user
            comment.save()
            return redirect('post_detail', post_id=post.id)  # Refresh the page

    else:
        form = f.CommentForm()

    return render(request, "post.html", {"post": post, "comments": comments, "form": form})


@login_required(login_url='/users/login')
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, post_id=post_id)

    # Ensure the user is authorized to delete the comment
    if request.user == comment.user:
        comment.delete()

    return redirect("post_detail", post_id=post_id)

@login_required(login_url='/users/login')
def create_post(request):
    if request.method == "POST":
        form = f.PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Assign the current user
            post.save()
            return redirect("/profile")  # Redirect to profile after posting
        else:
            print(form.errors)
    else:
        form = f.PostForm()

    return render(request, "create_post.html", {"form": form})

@login_required(login_url='/users/login')
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Ensure the current user is the owner
    if post.author != request.user:
        return redirect("/profile")

    if request.method == "POST":
        form = f.PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("/profile")
    else:
        form = f.PostForm(instance=post)

    return render(request, "edit_post.html", {"form": form})


@login_required(login_url='/users/login')
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Ensure only the post owner can delete
    if post.author != request.user:
        return redirect("/profile")

    if request.method == "POST":
        post.delete()
        
        # Handle AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({"success": True, "message": "Post deleted successfully!"})

        return redirect("/profile")

    return redirect("/profile")  # No need for a separate delete page

@login_required(login_url='/users/login')
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    if post.likes.filter(id=user.id).exists():
        post.likes.remove(user)  # Unlike if already liked
    else:
        post.likes.add(user)
        post.dislikes.remove(user)  # Remove dislike if previously disliked

    return JsonResponse({
        "likes": post.total_likes(),
        "dislikes": post.total_dislikes(),
        "user_liked": post.likes.filter(id=user.id).exists(),
        "user_disliked": post.dislikes.filter(id=user.id).exists(),
    })

@login_required(login_url='/users/login')
def dislike_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    if post.dislikes.filter(id=user.id).exists():
        post.dislikes.remove(user)  # Remove dislike if already disliked
    else:
        post.dislikes.add(user)
        post.likes.remove(user)  # Remove like if previously liked

    return JsonResponse({
        "likes": post.total_likes(),
        "dislikes": post.total_dislikes(),
        "user_liked": post.likes.filter(id=user.id).exists(),
        "user_disliked": post.dislikes.filter(id=user.id).exists(),
    })


