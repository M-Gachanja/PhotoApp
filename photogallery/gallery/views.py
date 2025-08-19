from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, PhotoForm
from .models import Photo, Tag, UserProfile
from PIL import Image

def save(self, *args, **kwargs):
    super().save(*args, **kwargs)
    
    if self.profile_picture:
        img = Image.open(self.profile_picture.path)
        
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_picture.path)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create user profile
            UserProfile.objects.create(user=user)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            
            # Auto-login after registration
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'gallery/register.html', {'form': form})

def custom_login(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                
                # Redirect to next page if provided, otherwise home
                next_page = request.GET.get('next')
                if next_page:
                    return redirect(next_page)
                return redirect('home')
    else:
        form = AuthenticationForm()
    
    return render(request, 'gallery/login.html', {'form': form})

def custom_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.userprofile
        )
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.userprofile)
    
    # Check if profile picture exists
    has_profile_picture = bool(request.user.userprofile.profile_picture)
    
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'has_profile_picture': has_profile_picture
    }
    
    return render(request, 'gallery/profile.html', context)

def home(request):
    photos = Photo.objects.all().order_by('-uploaded_at')
    tags = Tag.objects.all().order_by('name')
    
    # Filter by tag if provided
    tag_filter = request.GET.get('tag')
    if tag_filter:
        photos = photos.filter(tags__name=tag_filter)
    
    context = {
        'photos': photos,
        'tags': tags,
        'selected_tag': tag_filter
    }
    return render(request, 'gallery/home.html', context)

def photo_detail(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    is_liked = False
    if photo.likes.filter(id=request.user.id).exists():
        is_liked = True
    
    context = {
        'photo': photo,
        'is_liked': is_liked,
        'total_likes': photo.total_likes()
    }
    return render(request, 'gallery/photo_detail.html', context)

@login_required
def like_photo(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    if photo.likes.filter(id=request.user.id).exists():
        photo.likes.remove(request.user)
    else:
        photo.likes.add(request.user)
    return redirect('photo_detail', pk=pk)

@login_required
def upload_photo(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.uploaded_by = request.user
            photo.save()
            form.save_m2m()  # Save many-to-many relationships (tags)
            messages.success(request, 'Photo uploaded successfully!')
            return redirect('photo_detail', pk=photo.pk)
    else:
        form = PhotoForm()
    return render(request, 'gallery/upload_photo.html', {'form': form})

def tags_list(request):
    tags = Tag.objects.all().order_by('name')
    # Count photos for each tag
    tags_with_count = []
    for tag in tags:
        photo_count = Photo.objects.filter(tags=tag).count()
        tags_with_count.append({
            'tag': tag,
            'photo_count': photo_count
        })
    
    context = {
        'tags_with_count': tags_with_count
    }
    return render(request, 'gallery/tags_list.html', context)