from django.db import models
from django.urls import reverse
from account.models import *

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    
class Language(models.Model):
    language = models.CharField(max_length=200)
    
    def __str__(self):
        return self.language
    
class Review(models.Model):
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(default=0)
    
    def __str__(self):
        return self.user.username
    
    
class Movie(models.Model):
    TAGS=(
        ('Movies','Movies'),
        ('Tvshows','Tvshows'),
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    Tagname = models.CharField(max_length=200, choices=TAGS)
    cast = models.CharField(max_length=1000)
    genre = models.ManyToManyField(Genre)
    overview = models.TextField()
    release_date = models.CharField(max_length=100)
    Language = models.ForeignKey(Language, on_delete=models.CASCADE, null=True)
    runtime = models.CharField(max_length=100)
    average_rating = models.FloatField()
    date_posted = models.DateTimeField(auto_now_add=True)
    thumbnail = models.ImageField(upload_to="image")
    imdb = models.URLField(max_length=500, null=True, blank=True)
    downloadlink = models.URLField(max_length=800, null=True, blank=True)
    iframe = models.CharField(max_length=1000, null=True, blank=True)
    
    def __str__(self):
        return self.name
    
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