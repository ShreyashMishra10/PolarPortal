from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import Category, Article, MediaItem, Event, Bookmark, ContactMessage, Subscriber
from .forms import ContactForm, SubscribeForm, ArticleForm, MediaForm


# ---------------------------------------------------------------
#  Public pages (anyone can see these)
# ---------------------------------------------------------------

def home(request):
    # only approved articles are shown on the website
    approved = Article.objects.filter(is_approved=True)

    context = {
        'featured_articles': approved.filter(is_featured=True)[:3],
        'categories': Category.objects.all(),
        'latest_media': MediaItem.objects.all()[:4],
        'upcoming_events': Event.objects.filter(date__gte=timezone.now())[:3],
        # numbers for the stats strip on the home page
        'article_count': approved.count(),
        'media_count': MediaItem.objects.count(),
        'event_count': Event.objects.count(),
        'category_count': Category.objects.count(),
    }
    return render(request, 'portal/home.html', context)


def article_list(request):
    articles = Article.objects.filter(is_approved=True)

    # read the filters from the URL, e.g. /articles/?q=ice&region=arctic
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    region = request.GET.get('region', '')

    if query:
        articles = articles.filter(
            Q(title__icontains=query) | Q(summary__icontains=query) | Q(content__icontains=query)
        )
    if category_id.isdigit():  # ignore anything that is not a number
        articles = articles.filter(category_id=category_id)
    if region:
        articles = articles.filter(region=region)

    context = {
        'articles': articles,
        'categories': Category.objects.all(),
        'query': query,
        'selected_category': category_id,
        'selected_region': region,
    }
    return render(request, 'portal/article_list.html', context)


def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk, is_approved=True)

    # count a view every time someone opens the article
    article.views += 1
    article.save()

    # show other articles from the same category
    related = Article.objects.filter(category=article.category, is_approved=True).exclude(pk=pk)[:3]

    # check if the logged-in user has already saved this article
    is_bookmarked = False
    if request.user.is_authenticated:
        is_bookmarked = Bookmark.objects.filter(user=request.user, article=article).exists()

    context = {
        'article': article,
        'related': related,
        'is_bookmarked': is_bookmarked,
    }
    return render(request, 'portal/article_detail.html', context)


def media_gallery(request):
    media_type = request.GET.get('type', '')
    items = MediaItem.objects.filter(is_approved=True)  # only show media the admin has approved
    if media_type:
        items = items.filter(media_type=media_type)

    context = {
        'items': items,
        'media_types': MediaItem.MEDIA_TYPES,
        'selected_type': media_type,
    }
    return render(request, 'portal/media.html', context)


def events(request):
    now = timezone.now()
    context = {
        'upcoming': Event.objects.filter(date__gte=now),
        'past': Event.objects.filter(date__lt=now).order_by('-date'),
    }
    return render(request, 'portal/events.html', context)


def about(request):
    return render(request, 'portal/about.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you! Your message has been sent. We will get back to you soon.')
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'portal/contact.html', {'form': form})


def subscribe(request):
    # the newsletter form is in the footer of every page
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You are subscribed! Polar news will reach your inbox.')
        else:
            messages.error(request, 'This email is invalid or already subscribed.')

    # send the user back to the page they were on
    return redirect(request.META.get('HTTP_REFERER', 'home'))


# ---------------------------------------------------------------
#  Sign up (login and logout use Django's built-in views, see urls.py)
# ---------------------------------------------------------------

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # log the new user in straight away
            messages.success(request, f'Welcome to PolarPortal, {user.username}!')
            return redirect('dashboard')
    else:
        form = UserCreationForm()

    return render(request, 'portal/signup.html', {'form': form})


# ---------------------------------------------------------------
#  Members-only features (@login_required sends guests to the login page)
# ---------------------------------------------------------------

@login_required
def dashboard(request):
    my_articles = Article.objects.filter(submitted_by=request.user)
    my_bookmarks = Bookmark.objects.filter(user=request.user, article__is_approved=True).order_by('-saved_at')
    my_media = MediaItem.objects.filter(submitted_by=request.user)

    context = {
        'my_articles': my_articles,
        'my_media': my_media,
        'my_bookmarks': my_bookmarks,
        'approved_count': my_articles.filter(is_approved=True).count(),
        'pending_count': my_articles.filter(is_approved=False).count(),
    }

    # admins (staff users) also see the whole website's data on their dashboard
    if request.user.is_staff:
        context['site_articles'] = Article.objects.filter(is_approved=True).count()
        context['site_pending'] = Article.objects.filter(is_approved=False).order_by('-created_at')
        context['site_pending_media'] = MediaItem.objects.filter(is_approved=False)
        context['site_users'] = User.objects.count()
        context['site_subscribers'] = Subscriber.objects.count()
        context['site_messages'] = ContactMessage.objects.order_by('-sent_at')[:5]
        context['site_message_count'] = ContactMessage.objects.count()

    return render(request, 'portal/dashboard.html', context)


@login_required
def approve_article(request, pk):
    # only admins can approve, and only with the POST button on the dashboard
    if request.user.is_staff and request.method == 'POST':
        article = get_object_or_404(Article, pk=pk)
        article.is_approved = True
        article.save()
        messages.success(request, f'"{article.title}" is now live on the website.')
    return redirect('dashboard')


@login_required
def approve_media(request, pk):
    # same as approve_article, but for photos, videos, podcasts and documents
    if request.user.is_staff and request.method == 'POST':
        item = get_object_or_404(MediaItem, pk=pk)
        item.is_approved = True
        item.save()
        messages.success(request, f'"{item.title}" is now in the Media Gallery.')
    return redirect('dashboard')


@login_required
def upload_media(request):
    if request.method == 'POST':
        form = MediaForm(request.POST, request.FILES)  # request.FILES holds the uploaded file
        if form.is_valid():
            item = form.save(commit=False)
            item.submitted_by = request.user
            item.is_approved = request.user.is_staff  # admin uploads go live at once, others wait for approval
            item.save()
            if item.is_approved:
                messages.success(request, 'Media added to the gallery!')
                return redirect('media')
            messages.success(request, 'Media uploaded! It will appear in the gallery after admin approval.')
            return redirect('dashboard')
    else:
        form = MediaForm()

    return render(request, 'portal/upload_media.html', {'form': form})


@login_required
def submit_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)  # request.FILES holds the uploaded cover image
        if form.is_valid():
            article = form.save(commit=False)  # don't save yet, we fill a few more fields first
            article.submitted_by = request.user
            article.author = request.user.username
            article.is_approved = request.user.is_staff  # admin articles go live at once, others wait for approval
            article.save()
            if article.is_approved:
                messages.success(request, 'Article published!')
                return redirect('article_detail', pk=article.pk)
            messages.success(request, 'Article submitted! It will appear on the website after admin approval.')
            return redirect('dashboard')
    else:
        form = ArticleForm()

    return render(request, 'portal/submit_article.html', {'form': form})


@login_required
def toggle_bookmark(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if request.method == 'POST':
        bookmark = Bookmark.objects.filter(user=request.user, article=article)
        if bookmark.exists():
            bookmark.delete()
            messages.success(request, 'Removed from your bookmarks.')
        else:
            Bookmark.objects.create(user=request.user, article=article)
            messages.success(request, 'Saved to your bookmarks!')

    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))
