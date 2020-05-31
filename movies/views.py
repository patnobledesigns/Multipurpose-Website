from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *
from .forms import *
from news.models import *
from news.forms import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView
from django.db.models import Count, Q
from django.db.models.aggregates import Avg

# Create your views here.

def get_language_count():
    queryset = Movie.objects.values('Language__language').annotate(Count('Language__language'))
    return queryset

def search_home(request):
    queryset = Movie.objects.all()
    post = Post.objects.all()
    query = request.GET.get('q')
    
    if query:
        queryset = queryset.filter( 
            Q(name__icontains=query) |
            Q(overview__icontains=query)
        ).distinct()
        if query:
            post = post.filter(
                Q(title__icontains=query) 
            )
        
    context = {
        'queryset': queryset,
        'post': post,
    } 
    return render(request, 'movies/homesearch.html', context)


class Home(ListView):
    model = Movie
    template_name = 'movies/index.html'
    context_object_name = 'post_list'
    paginate_by = 4
    
    def get_queryset(self):
        return Post.objects.all()
    
    def get_context_data(self, **kwargs):
        most_recent = Post.objects.order_by('-timestamp')[:3]
        image = ImageSlide.objects.all()
        language_count = get_language_count()
        movies = Movie.objects.all().order_by('-date_posted')[0:6]
        context = super().get_context_data(**kwargs)
        context["movie"] = movies
        context["language_count"] = language_count
        context["most_recent"] = most_recent
        context["image"] = image
        return context


class Movies(ListView):
    model = Movie
    template_name = 'movies/movies.html'
    context_object_name = 'movies'
    paginate_by = 12

    def get_queryset(self):
        query = self.request.GET.get('q')
        allmovies = None
        if query: 
            allmovies = Movie.objects.filter(name__icontains=query)
        else:
            allmovies = Movie.objects.filter(Tagname="Movies").order_by('-date_posted')
        return allmovies
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Movies'
        return context
    
@login_required(login_url='login')
def movies_detail(request, slug):
    movies = get_object_or_404(Movie, slug=slug)
    reviews = Review.objects.filter(movie__slug=slug).order_by('-date_posted')
    
    average = reviews.aggregate(Avg("rating"))["rating__avg"]
    if average == None:
        average = 0
    average = round(average, 1)
    try:
        if request.method == "POST":
            form = MovieReviewForm(request.POST or None)
            if form.is_valid():
                data = form.save(commit=False)
                data.comment = request.POST["comment"]
                data.rating = request.POST["rating"]
                data.user = request.user
                data.movie = movies
                data.save()
                return redirect('allmoviesInfo', slug)
        else:
            form = MovieReviewForm(request.POST or None)
    except ValueError:
        return redirect('login')

    context={
        'movies': movies,
        'form': form, 
        'reviews': reviews, 
        'average': average
    }
    return render(request, 'movies/details.html', context)


def edit_review(request, slug, pk):
    if request.user.is_authenticated:
        movie = Movie.objects.get(slug=slug)
        review = Review.objects.get(movie=movie, pk=pk)

        if request.user == review.user:
            if request.method == "POST":
                form = MovieReviewForm(request.POST or None, instance=review)
                if form.is_valid():
                    data = form.save(commit=False)
                    data.save()
                    return redirect('allmoviesInfo', slug)
            else:
                form = MovieReviewForm(instance=review)
            return render(request, 'movies/editreview.html', {'form': form})
        else:
            return redirect('allmoviesInfo', pk)
    else:
        return redirect('login')
    
def delete_review(request, slug, pk):
    if request.user.is_authenticated:
        movie = Movie.objects.get(slug=slug)
        review = Review.objects.get(movie=movie, pk=pk)

        if request.user == review.user:
            review.delete() 
        return redirect('allmoviesInfo', slug)
    else:
        return redirect('login')

        
def create_movie(request):
    if not request.user.is_staff or not request.user.is_superuser:
        return redirect('allmovies')
    else:
        title = 'ADD'
        
        if request.method == "POST":
            form = CreateMovieForm(request.POST or None, request.FILES or None)
            if form.is_valid():
                form.save()
                moviename = form.cleaned_data.get('name')
                
                messages.success(request, f'{moviename} was Added!')
                return redirect("createmovie")
        else:
            form = CreateMovieForm()
            
        context = {
            "form": form,
            "new": title
        }
        return render(request, 'movies/createmovie.html', context)

def update_movie(request, slug):
    if not request.user.is_staff or not request.user.is_superuser:
        return redirect('allmovies')   
    else: 
        title = 'UPDATE'
        movies = get_object_or_404(Movie, slug=slug)
        
        if request.method == "POST":
            form = CreateMovieForm(request.POST or None, request.FILES or None, instance=movies)
            if form.is_valid():
                form.save()
                moviename = form.cleaned_data.get('name')
                
                messages.success(request, f'{moviename} has been updated!')
                return redirect("allmovies")
        else:
            form = CreateMovieForm(instance=movies)
            
        context = {
            "form": form,
            "new": title
        }
        return render(request, 'movies/createmovie.html', context)

def delete_movie(request, slug):
    if not request.user.is_staff or not request.user.is_superuser:
        return redirect('allmovies')
    else:
        movies = get_object_or_404(Movie, slug=slug)

        if request.method == 'POST':
            
            movies.delete()
            return redirect('allmovies')

        context = {
            'movie' : movies
        }
        return render(request, 'movies/delete.html', context)
    