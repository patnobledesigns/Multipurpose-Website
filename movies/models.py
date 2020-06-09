from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify
from account.models import *

# Create your models here.
class Review(models.Model):
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(default=0)
    
    def __str__(self):
        return self.user.username
    
class Movie(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True, unique=True)
    slug = models.SlugField(max_length=1000, blank=True)
    Tagname = models.CharField(max_length=200, null=True, blank=True, default="Movie")
    star = models.CharField(max_length=500, null=True, blank=True)
    genre = models.CharField(max_length=500, null=True, blank=True)
    overview = models.TextField(null=True, blank=True, unique=True)
    release_date = models.CharField(max_length=100, null=True, blank=True)
    language = models.CharField(max_length=200, null=True, blank=True)
    runtime = models.CharField(max_length=100,null=True, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    thumbnail = models.URLField(max_length=1000, null=True, blank=True)
    imdb = models.URLField(max_length=500, null=True, blank=True)
    download_link = models.URLField(max_length=800, null=True, blank=True, unique=True)
    iframe = models.CharField(max_length=1000, null=True, blank=True)
    source = models.CharField(max_length=500, null=True, blank=True)
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Slugify name if it doesn't exist. IMPORTANT: doesn't check to see
        if slug is a dupe!
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super(Movie, self).save(*args, **kwargs)

    
    def get_absolute_url(self):
        return reverse("allmoviesInfo", kwargs={"slug": self.slug})
    
    @property
    def comment_count(self):
        return Review.objects.filter(movie=self).count()

   
class ImageSlide(models.Model):
    thumbnail = models.URLField(max_length=1000, null=True, blank=True)
    title = models.CharField(max_length=500, null=True, blank=True)
    
    def __str__(self):
        return self.title