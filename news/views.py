from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import *
from django.db.models import Count, Q
from .forms import CommentForm, PostForm
from movies.views import get_language_count
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.
def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None


@login_required(login_url='login')
def news_detail(request, slug):
    language_count =  get_language_count()
    most_recent = Post.objects.order_by('-timestamp')[:3]
    post = get_object_or_404(Post, slug=slug)
    
    if request.user.is_authenticated:
        PostView.objects.get_or_create(user=request.user, post=post)
    
    form = CommentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid:
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse('newsInfo', kwargs={
                'slug': post.slug
            }))
            
    context={
        'title': 'News',
        'post': post,
        'language_count': language_count,
        'most_recent': most_recent,
        'form': form,
    }
    return render(request, 'news/NewsFeed.html', context)

def comment_delete(request, slug, comment_id):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, slug=slug)
        comment = Comment.objects.get(post=post, pk=comment_id)

    if request.user == (comment.user or comment.user.is_staff()):
        comment.delete() 
        return redirect(reverse('newsInfo', kwargs={
                'slug': post.slug
            }))
    else:
        return redirect('login')


def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')

    
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        ).distinct()
        
        
    context = {
        'queryset': queryset,
    } 
    return render(request, 'movies/search_result.html', context)

def news_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        return redirect('home')
    else:
        title = 'Create'
        form = PostForm(request.POST or None, request.FILES or None)
        author = get_author(request.user)
        if request.method == "POST":
            if form.is_valid():
                form.instance.author = author
                form.save()
                messages.success(request, f'Post Has been Created')
                return redirect(reverse("newsInfo", kwargs={
                    'slug': form.instance.slug
                }))
        context = {
            'title': title,
            'post': 'Post',
            'form': form
        }
        return render(request, 'news/news_create.html', context)

def news_update(request, slug):
    if not request.user.is_staff or not request.user.is_superuser:
        return redirect(reverse("newsInfo", kwargs={
                    'slug': slug
                }))
    else:    
        title = 'Update'
        post = get_object_or_404(Post, slug=slug)
        form = PostForm(request.POST or None, request.FILES or None, instance=post)
        author = get_author(request.user)
        if request.method == "POST":
            if form.is_valid():
                form.instance.author = author
                form.save()
                messages.success(request, f'Post Has been updated')
                return redirect(reverse("newsInfo", kwargs={
                    'slug': form.instance.slug
                }))
        context = {
            'title': title,
            'post': 'Update',
            'form': form,
        }
        return render(request, 'news/news_create.html', context)

def news_delete(request, slug):
    if not request.user.is_staff or not request.user.is_superuser:
        return redirect(reverse("newsInfo", kwargs={
                    'slug': slug
                }))
    else:
        post = get_object_or_404(Post, slug=slug)
        
        if request.method == 'POST':
            post.delete()
            return redirect('/')
            
        context = {
                'post' : post  
        }
        return render(request, 'news/delete.html', context)