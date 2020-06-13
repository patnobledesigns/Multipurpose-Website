from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import *
from django.db.models import Count, Q
from .forms import CommentForm, PostForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from taggit.models import Tag
from urllib.parse import quote_plus
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None

def get_category_count():
    queryset = Post.objects.values('category__name').annotate(Count('category__name'))
    return queryset


def newsView(request):
    bus = Category.objects.get(name="Business")
    business = bus.post_set.all().order_by('-timestamp')[:4]
    spo = Category.objects.get(name="Sport")
    Sport = spo.post_set.all().order_by('-timestamp')[:4]
    pol = Category.objects.get(name="Politics")
    Politics = pol.post_set.all().order_by('-timestamp')[:4]
    tech = Category.objects.get(name="Technology")
    Technology = tech.post_set.all().order_by('-timestamp')[:4]
    nat = Category.objects.get(name="National News")
    National = nat.post_set.all().order_by('-timestamp')[:4]
    ent = Category.objects.get(name="Entertainment")
    Entertainment = ent.post_set.all().order_by('-timestamp')[:4]
    edu = Category.objects.get(name="Education")
    Education = edu.post_set.all().order_by('-timestamp')[:4]
    gis = Category.objects.get(name="Gist")
    Gist = gis.post_set.all().order_by('-timestamp')[:4]
    context={
        'title': 'News Update',
        'business': business,
        'Sport': Sport,
        'Politics': Politics,
        'Education': Education,
        'Entertainment': Entertainment,
        'National': National,
        'Technology': Technology,
        'Gist': Gist,
    }
    return render(request, 'news/news.html', context)


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
        'slug': slug,
        'category_count': category_count,
        'most_recent': most_recent,
        'form': form,
        'tags': tags,
        'share_string': share_string,
    }
    return render(request, 'news/NewsFeed.html', context)


# class Postcategory(DetailView):
#     model = Post
#     template_name = 'news/postCategory.html'
#     context_object_name = 'post'
#     paginate_by = 6
#     slug_field = "slug"
#     slug_url_kwarg = "article_slug"
    
#     def get_object(self):
#         category = get_object_or_404(Category, slug=self.kwargs['slug'])
#         return category
    
#     def get_queryset(self):
#         slug=self.kwargs.get("slug")
#         if slug:
#             post  = Post.objects.all()
#             category = get_object_or_404(Category, slug=slug)
#             posts = post.filter(category=category).order_by('-id')
#             return posts
    
#     def get_context_data(self, **kwargs):
#         category_count =  get_category_count()
#         most_recent = Post.objects.order_by('-timestamp')[:3]
#         categories = Category.objects.all()
#         tags = Tag.objects.all()
#         context = super().get_context_data(**kwargs)
#         context["category_count"] = category_count
#         context["most_recent"] = most_recent
#         context["tags"] = Tag.objects.all()
#         context["categories"] = categories
#         return context

def postCategory(request, category_slug):
    category_count =  get_category_count()
    most_recent = Post.objects.order_by('-timestamp')[:3]
    categories = Category.objects.all()
    post  = Post.objects.all()
    tags = Tag.objects.all()

    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        posts = post.filter(category=category).order_by('-id')
        page_request_var = 'page'  
        page = request.GET.get(page_request_var)

        paginator = Paginator(posts, 6)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
            print(users)
        
    context = {
        'categories': categories,
        'page_obj': users,
        'category': category,
        'category_count': category_count,
        'most_recent': most_recent,
        'tags': tags,
        'title': category,
        'page_request_var': page_request_var
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