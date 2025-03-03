from django.urls import path, include

from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('about/', views.about),
    path('posts/', include('posts.urls')),
    path('users/', include('users.urls')),  # Include your user authentication URLs
    path('profile/', views.profile),
    path('users/<str:username>/', views.user_profile, name='user_profile'),

]
