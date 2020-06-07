from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import *
from django.db.models import Count, Q
from .forms import CommentForm, PostForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from taggit.models import Tag
from urllib.parse import quote_plus

# Create your views here.
def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None

def get_category_count():
    queryset = Post.objects.values('category__name').annotate(Count('category__name'))
    return queryset

@login_required(login_url='login')
def news_detail(request, slug):
    category_count =  get_category_count()
    most_recent = Post.objects.order_by('-timestamp')[:3]
    post = get_object_or_404(Post, slug=slug)
    tags = Tag.objects.all()
    share_string = quote_plus(post.content)
    
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
        'title': post,
        'post': post,
        'category_count': category_count,
        'most_recent': most_recent,
        'form': form,
        'tags': tags,
        'share_string': share_string,
    }
    return render(request, 'news/NewsFeed.html', context)

def postCategory(request, category_slug):
    category_count =  get_category_count()
    most_recent = Post.objects.order_by('-timestamp')[:3]
    categories = Category.objects.all()
    post  = Post.objects.all()
    tags = Tag.objects.all()
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        posts = post.filter(category=category)
    context = {
        'categories': categories,
        'post': posts,
        'category': category,
        'category_count': category_count,
        'most_recent': most_recent,
        'tags': tags,
        'title': category,
    }
    return render(request, 'news/postCategory.html', context)
    

def postTag(request, slug):
    category_count =  get_category_count()
    most_recent = Post.objects.order_by('-timestamp')[:3]
    tags = Tag.objects.all()
    post  = Post.objects.all()
    posttags = Post.objects.filter(tags__slug=slug)
    
    context = {
        'tags': tags,
        'posttags': posttags,
        'category_count': category_count,
        'post': post,
        'most_recent': most_recent,
        'title': 'Tags',
    }
    return render(request, 'news/tags.html', context)


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