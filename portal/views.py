from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import Category, Article, MediaItem, Event, Bookmark
from .forms import ContactForm, SubscribeForm, ArticleForm


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
    items = MediaItem.objects.all()
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

    context = {
        'my_articles': my_articles,
        'my_bookmarks': my_bookmarks,
        'approved_count': my_articles.filter(is_approved=True).count(),
        'pending_count': my_articles.filter(is_approved=False).count(),
    }
    return render(request, 'portal/dashboard.html', context)


@login_required
def submit_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)  # don't save yet, we fill a few more fields first
            article.submitted_by = request.user
            article.author = request.user.username
            article.is_approved = False  # admin has to approve it first
            article.save()
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
