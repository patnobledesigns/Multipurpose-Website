from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(Language)
admin.site.register(Review)
admin.site.register(ImageSlide)