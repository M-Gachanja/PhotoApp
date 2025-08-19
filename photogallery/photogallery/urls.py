"""
URL configuration for photogallery project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from gallery import views as gallery_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', gallery_views.home, name='home'),
    path('register/', gallery_views.register, name='register'),
    path('login/', gallery_views.custom_login, name='login'),
    path('logout/', gallery_views.custom_logout, name='logout'),
    path('profile/', gallery_views.profile, name='profile'),
    path('photo/<int:pk>/', gallery_views.photo_detail, name='photo_detail'),
    path('photo/like/<int:pk>/', gallery_views.like_photo, name='like_photo'),
    path('upload/', gallery_views.upload_photo, name='upload_photo'),
    path('tags/', gallery_views.tags_list, name='tags_list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
