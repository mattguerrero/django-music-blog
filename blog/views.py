from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post

import operator
from django.db.models import Q

####### IMPORTS FOR SPOTIFY API

import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

SPOTIFY_ID = os.environ.get('SPOTIFY_ID')
SPOTIFY_SECRET = os.environ.get('SPOTIFY_SECRET')

ccm = SpotifyClientCredentials(client_id=SPOTIFY_ID,
                                client_secret=SPOTIFY_SECRET)

#######


# Create your views here.
def home(request):
    context = {
        'posts': Post.objects.all(),
    }
    return render(request, 'blog/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date']
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date')


class SearchPostListView(ListView):
    model = Post
    template_name = 'blog/post_search.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('q')
        
        if query:
            query_words = query.split(',')
            query_words = [word.lower().strip() for word in query_words]
            
            # get all posts with at least one of the searched tags
            initial = Post.objects.filter(tags__slug__in=query_words).order_by('-date')
            result = [post for post in initial]
            # filter posts if they don't contain all the tags
            for post in initial:
                for tag in query_words:
                    if tag not in post.tags.slugs():
                        result.remove(post)

            result = list(set(result)) #remove duplicates
            return result
        else:
            return Post.objects.all()



class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['link', 'rating', 'content', 'tags']

    def form_valid(self, form):
        spotify = spotipy.Spotify(client_credentials_manager=ccm)

        form.instance.author = self.request.user

        url = form.cleaned_data['link']
        if "artist/" in url:
            results = spotify.artist(url)
            form.instance.category = results["type"]
            form.instance.title = results["name"]
            form.instance.artist = results["name"]
        elif "album/" in url:
            results = spotify.album(url)
            form.instance.category = results["type"]
            form.instance.title = results["name"]
            form.instance.artist = results["artists"][0]["name"]
        elif "track/" in url:
            results = spotify.track(url)
            form.instance.category = results["type"]
            form.instance.title = results["name"]
            form.instance.artist = results["artists"][0]["name"]

        if "embed/" not in url:
            form.instance.link = url[:25] + "embed/" + url[25:]

        #######
        form.save()
        form.instance.tags.add(form.instance.title, 
                                form.instance.artist,
                                form.instance.category)
        #######

        return HttpResponseRedirect(form.instance.get_absolute_url())

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['link', 'rating', 'content', 'tags']

    def form_valid(self, form):
        form.instance.author = self.request.user
        
        if "embed/" not in form.cleaned_data['link']:
            form.instance.link = form.cleaned_data['link'][:25] + "embed/" + form.cleaned_data['link'][25:]
        
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False



class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = "/"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})