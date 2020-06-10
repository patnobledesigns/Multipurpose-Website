from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import *


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Author.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.author.save()
    
def customer_profile(sender, instance, created, **kwargs):
	if created: 
		group = Group.objects.get(name='user')
		instance.groups.add(group)
		print('Added to Group')

post_save.connect(customer_profile, sender=User)
    



