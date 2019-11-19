from django.urls import path
from django.conf.urls import url
from . import views
from .feeds import LatestPostFeed
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

app_name = 'video'
urlpatterns = [
    path('', views.index, name='index'),
    path('movie/<int:pk>', views.movie, name='movie'),
    path('movie/<int:pk>/eval', views.movie_eval, name='movie_eval'),
    path('category/<str:c>', views.search_category, name='category'),
    path('tag/<str:t>', views.search_tag, name='tag'),
    path('search/', views.search_form, name='search'),
    path('contact/', views.page_contact, name='contact'),
    path('about/', views.page_about, name='about'),
    path('latest/feed/', LatestPostFeed(), name='feed'),
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]