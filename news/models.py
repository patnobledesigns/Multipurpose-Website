from django.db import models
from tinymce import HTMLField
from ckeditor.fields import RichTextField
from django.urls import reverse
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from account.models import *

from taggit.managers import TaggableManager

# Create your models here.
    
class PostView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    post = models.ForeignKey('Post', related_name='comments', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username  

class Category(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    slug = models.SlugField(max_length = 100, null=True, blank=True)
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        
    def get_category_url(self):
        return reverse("postCategory", kwargs={"slug": self.slug})
    
    def __str__(self):
        return self.name
   
class Post(models.Model):
    title = models.CharField(max_length=500, null=True, blank=True, unique=True)
    slug = models.SlugField(max_length=500, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    content = RichTextField(null=True, blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    thumbnail = models.URLField(max_length=1000, null=True, blank=True)
    previous_post = models.ForeignKey('self', related_name='previous', on_delete=models.SET_NULL, blank =True, null=True)
    next_post = models.ForeignKey('self', related_name='next', on_delete=models.SET_NULL, blank =True, null=True)
    tags = TaggableManager()

    def __str__(self):
        return self.title
        
    
    def save(self, *args, **kwargs):
        """
        Slugify name if it doesn't exist. IMPORTANT: doesn't check to see
        if slug is a dupe!
        """
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("newsInfo", kwargs={"slug": self.slug})
    
    def get_update_url(self):
        return reverse("news-update", kwargs={"slug": self.slug})
    
    def get_delete_url(self):
        return reverse("news-delete", kwargs={"slug": self.slug})
    
    @property
    def get_comments(self):
        return self.comments.all().order_by('-timestamp')

    @property
    def comment_count(self):
        return Comment.objects.filter(post=self).count()
    
    @property
    def view_count(self):
        return PostView.objects.filter(post=self).count()