from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(default="profile1.png")

    def __str__(self):
        return f'{self.user.username} Profile'
    
    def get_delete_url(self):
        return reverse("user_delete", kwargs={"pk": self.pk})