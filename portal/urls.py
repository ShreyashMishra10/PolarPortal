from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    # public pages
    path('', views.home, name='home'),
    path('articles/', views.article_list, name='article_list'),
    path('articles/<int:pk>/', views.article_detail, name='article_detail'),
    path('media/', views.media_gallery, name='media'),
    path('events/', views.events, name='events'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('subscribe/', views.subscribe, name='subscribe'),

    # accounts - login and logout come ready-made with Django
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='portal/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # members only
    path('dashboard/', views.dashboard, name='dashboard'),
    path('submit/', views.submit_article, name='submit_article'),
    path('articles/<int:pk>/bookmark/', views.toggle_bookmark, name='toggle_bookmark'),
    path('media/upload/', views.upload_media, name='upload_media'),

    # admin only
    path('articles/<int:pk>/approve/', views.approve_article, name='approve_article'),
    path('media/<int:pk>/approve/', views.approve_media, name='approve_media'),
]
