from django.db import models
from tinymce import HTMLField
from django.urls import reverse
from django.contrib.auth.models import User
from account.models import *

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

   
class Post(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    content = HTMLField()
    # comment_count = models.IntegerField(default = 0)
    # view_count = models.IntegerField(default = 0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    thumbnail = models.ImageField()
    previous_post = models.ForeignKey('self', related_name='previous', on_delete=models.SET_NULL, blank =True, null=True)
    next_post = models.ForeignKey('self', related_name='next', on_delete=models.SET_NULL, blank =True, null=True)


    def __str__(self):
        return self.title
    
    def snippet(self):
        return f'{self.overview[:70]} ...'
    
    def get_absolute_url(self):
        return reverse("newsInfo", kwargs={"pk": self.pk})
    
    def get_update_url(self):
        return reverse("news-update", kwargs={"pk": self.pk})
    
    def get_delete_url(self):
        return reverse("news-delete", kwargs={"pk": self.pk})
    
    @property
    def get_comments(self):
        return self.comments.all().order_by('-timestamp')

    @property
    def comment_count(self):
        return Comment.objects.filter(post=self).count()
    
    @property
    def view_count(self):
        return PostView.objects.filter(post=self).count()