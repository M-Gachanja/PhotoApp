from django.contrib import admin
from .models import Photo, Tag, UserProfile

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']
    search_fields = ['name']

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ['title', 'uploaded_by', 'uploaded_at']
    list_filter = ['tags', 'uploaded_at']
    filter_horizontal = ['tags']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'id']

admin.site.site_header = "Photo Gallery Admin"