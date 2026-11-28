from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Used by both articles and media so we can filter by pole
REGION_CHOICES = [
    ('arctic', 'Arctic'),
    ('antarctic', 'Antarctic'),
    ('both', 'Both Poles'),
]


class Category(models.Model):
    """A topic in the knowledge repository, e.g. Glaciology, Wildlife."""
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=10, default='❄️', help_text='An emoji shown on the card')
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def approved_count(self):
        # only count articles that are visible on the website
        return self.articles.filter(is_approved=True).count()


class Article(models.Model):
    """A knowledge article - the main content of the repository."""
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='articles')
    region = models.CharField(max_length=20, choices=REGION_CHOICES, default='both')
    icon = models.CharField(max_length=10, blank=True, help_text='Emoji for this article. Leave empty to use the category icon')
    image = models.ImageField(upload_to='article_images/', blank=True, help_text='Optional cover photo. Without one, the card shows the emoji.')
    author = models.CharField(max_length=100)
    summary = models.CharField(max_length=300)
    content = models.TextField()
    is_featured = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    # the real published research this article is based on
    source = models.CharField(max_length=300, blank=True, help_text='e.g. Rantanen, M. et al. (2022). Title. Journal.')
    source_url = models.URLField(blank=True, help_text='Link to the original paper or official page')

    # for articles sent in by logged-in users
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    is_approved = models.BooleanField(default=True, help_text='Only approved articles are shown on the website')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_icon(self):
        # use the article's own icon, or the category icon if it doesn't have one
        return self.icon or self.category.icon

    def reading_time(self):
        # average person reads about 200 words per minute
        words = len(self.content.split())
        return max(1, words // 200)


class Bookmark(models.Model):
    """An article saved by a user to read later."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # a user can bookmark the same article only once
        unique_together = ['user', 'article']

    def __str__(self):
        return f'{self.user.username} saved {self.article.title}'


class MediaItem(models.Model):
    """Photos, videos, podcasts and documents shared by the portal."""
    MEDIA_TYPES = [
        ('photo', 'Photo'),
        ('video', 'Video'),
        ('podcast', 'Podcast'),
        ('document', 'Document'),
    ]

    title = models.CharField(max_length=200)
    media_type = models.CharField(max_length=20, choices=MEDIA_TYPES)
    region = models.CharField(max_length=20, choices=REGION_CHOICES, default='both')
    description = models.TextField()
    file = models.FileField(upload_to='media_files/', blank=True, help_text='Upload a photo, video (MP4) or PDF')
    link = models.URLField(blank=True, help_text='Or give a link, e.g. a YouTube video or a website')
    created_at = models.DateTimeField(default=timezone.now)

    # media uploaded by members waits for admin approval, just like articles
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    is_approved = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def icon(self):
        icons = {'photo': '📷', 'video': '🎬', 'podcast': '🎧', 'document': '📄'}
        return icons.get(self.media_type, '📁')

    def is_image(self):
        # only show the uploaded file as a picture if it really is one
        name = self.file.name.lower()
        return name.endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp'))

    def is_video(self):
        # uploaded video files can be played straight on the card
        name = self.file.name.lower()
        return name.endswith(('.mp4', '.webm', '.ogg', '.mov'))

    def youtube_id(self):
        # takes the video id out of a YouTube link so we can show the video on the card
        # e.g. https://www.youtube.com/watch?v=abc123  or  https://youtu.be/abc123  ->  abc123
        link = self.link
        if 'youtube.com/watch?v=' in link:
            return link.split('v=')[1].split('&')[0]
        if 'youtu.be/' in link:
            return link.split('youtu.be/')[1].split('?')[0]
        return ''


class Event(models.Model):
    """Outreach events - talks, workshops, webinars."""
    title = models.CharField(max_length=200)
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    is_online = models.BooleanField(default=False)
    description = models.TextField()

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    """Messages sent from the Contact page. Admin can read them in the admin panel."""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.subject}'


class Subscriber(models.Model):
    """People who signed up for the newsletter in the footer."""
    email = models.EmailField(unique=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
