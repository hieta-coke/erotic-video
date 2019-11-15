from django.shortcuts import get_object_or_404, redirect, render, render_to_response
import operator
from django.db.models import Q
from django.http import HttpResponse
from .models import *
from .forms import *
from django.http import Http404
from django.core.paginator import Paginator

def index(request):
    movies = Movie.objects.all().order_by('-created_at')
    paginator = Paginator(movies, 20)
    p = request.GET.get('p')
    movies = paginator.get_page(p)
    movies.paginator.all_page = range(movies.paginator.num_pages)
    for movie in movies:
        movie.tag = movie.tag.split(',')
    content = {
        'page_title': 'RealVideo | リアルビデオ',
        'search_form': SearchForm(),
        'movies': movies,
    }
    return render(request, 'video/index.html', content)

def movie(request, pk):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            comment = form.cleaned_data['comment']
            movie = get_object_or_404(Movie, pk=pk)
            c = Comment(name=name, comment=comment, movie=movie)
            c.save()
        return redirect('video:movie', pk=pk)
    else:
        movie = get_object_or_404(Movie, pk=pk)
        movie.view += 1
        movie.save()
        comments = Comment.objects.filter(movie=movie).order_by('-created_at')
        origin_tags = "(" + movie.tag + ")".replace(",", "|")
        movies = Movie.objects.filter(tag__regex=origin_tags)
        for rm in movies:
            rm.tag = rm.tag.split(',')
        content = {
            'page_title': 'RealVideo | ' + movie.title,
            'search_form': SearchForm(),
            'comment_form': CommentForm(),
            'movie': movie,
            'relation': movies,
            'comments': comments,
        }
        return render(request, 'video/movie.html', content)

def movie_eval(request, pk):
    if request.method == 'POST':
        from django.http import QueryDict
        from json import dumps
        dic = QueryDict(request.body, encoding='utf-8')
        data = dic.get('eval')
        btn = get_object_or_404(Movie, pk=pk)
        if data == "good":
            btn.good += 1
            btn.save()
            cnt = btn.good
            return HttpResponse(dumps({"cnt": cnt}), content_type='application/json')
        elif data == "bad":
            btn.bad += 1
            btn.save()
            cnt = btn.bad
            return HttpResponse(dumps({"cnt": cnt}), content_type='application/json')
    return redirect('video:movie', pk=pk)
    
def search_category(request, c):
    category = get_object_or_404(Category, title=c)
    movies = Movie.objects.filter(category=category).order_by('-created_at')
    paginator = Paginator(movies, 20)
    p = request.GET.get('p')
    movies = paginator.get_page(p)
    movies.paginator.all_page = range(movies.paginator.num_pages)
    for movie in movies:
        movie.tag = movie.tag.split(',')
    content = {
        'page_title': 'RealVideo | カテゴリ >> ' + c,
        'search_form': SearchForm(),
        'search_title': 'カテゴリ >> ' + c,
        'movies': movies,
    }
    return render(request, 'video/index.html', content)

def search_tag(request, t):
    movies = Movie.objects.filter(tag__icontains=t).order_by('-created_at')
    if len(movies) == 0: raise Http404
    paginator = Paginator(movies, 20)
    p = request.GET.get('p')
    movies = paginator.get_page(p)
    movies.paginator.all_page = range(movies.paginator.num_pages)
    for movie in movies:
        movie.tag = movie.tag.split(',')
    content = {
        'page_title': 'RealVideo | タグ >> ' + t,
        'search_form': SearchForm(),
        'search_title': 'タグ >> ' + t,
        'movies': movies,
    }
    return render(request, 'video/index.html', content)

def search_form(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            txt = form.cleaned_data['squeeze']
            movies = Movie.objects.filter(title__icontains=txt).order_by('-created_at')
            if len(movies) == 0: raise Http404
            for movie in movies:
                movie.tag = movie.tag.split(',')
            content = {
                'page_title': 'RealVideo | リアルビデオ',
                'search_form': SearchForm(),
                'search_title': 'タイトル >> ' + txt,
                'movies': movies,
            }
            return render(request, 'video/index.html', content)
    return redirect('video:index')

def page_contact(request):
    if request.method == 'POST':
        pass
    else:
        content = {
            'page_title': 'RealVideo | お問い合わせ',
            'search_form': SearchForm(),
            'contact_form': ContactForm(),
        }
        return render(request, 'video/contact.html', content)

def page_about(request):
    content = {
        'page_title': 'RealVideo | このサイトについて',
        'search_form': SearchForm(),
    }
    return render(request, 'video/about.html', content)

# 404
def notfound(request, exception):
    content = {
        'page_title': 'RealVideo | 404 not found',
        'search_form': SearchForm(),
    }
    return render(request,'404.html', content)