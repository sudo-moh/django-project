from django.urls import path
from . import views  # Import views


urlpatterns = [
    path("", views.posts_list, name="posts"),  # List all posts
    path("new/", views.create_post, name="create_post"),  # Create a new post
    path("<int:post_id>/", views.post_detail, name="post_detail"),  # View a specific post
    path("<int:post_id>/edit/", views.edit_post, name="edit_post"),  # Edit a post
    path("<int:post_id>/delete/", views.delete_post, name="delete_post"),  # Delete a post
    path('<int:post_id>/like/', views.like_post, name='like_post'),
    path('<int:post_id>/dislike/', views.dislike_post, name='dislike_post'),
    path('<int:post_id>/delete-comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
]

