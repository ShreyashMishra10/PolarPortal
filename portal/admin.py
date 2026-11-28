from django.contrib import admin
from .models import Category, Article, MediaItem, Event, ContactMessage, Subscriber, Bookmark


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'region', 'author', 'is_approved', 'is_featured', 'views', 'created_at']
    list_filter = ['is_approved', 'category', 'region', 'is_featured']
    search_fields = ['title', 'summary', 'content', 'source']
    # lets the admin approve articles with a tick box right in the list
    list_editable = ['is_approved', 'is_featured']


@admin.register(MediaItem)
class MediaItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'media_type', 'region', 'submitted_by', 'is_approved', 'created_at']
    list_editable = ['is_approved']  # tick to approve straight from the list
    list_filter = ['is_approved', 'media_type', 'region']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'location', 'is_online']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'sent_at']


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ['user', 'article', 'saved_at']


admin.site.register(Subscriber)

admin.site.site_header = 'Polar Portal Admin'
admin.site.site_title = 'Polar Portal'
