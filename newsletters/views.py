from django.contrib import messages
from django.shortcuts import render
from .models import NewsletterUser
from .forms import NewsletterUserSignUpForm

# Create your views here.

def newsletter_subscribe(request):
    form = NewsletterUserSignUpForm(request.POST or None)
    
    if form.is_valid():
        data = form.save(commit=False)
        if NewsletterUser.objects.filter(email=data.email).exists():
            messages.warning(request, 'Email Already Exists', "alert alert-warning alert-dismissible")
        else:
            data.save()
            messages.success(request, 'Your Email has been submitted', "alert alert-success alert-dismissible")
    context = {
        'form': form,
    }
    template = "newsletters/subscribe.html"
    return render(request, template, context)

def newsletter_unsubscribe(request):
    form = NewsletterUserSignUpForm(request.POST or None)
    
    if form.is_valid():
        data = form.save(commit=False)
        if NewsletterUser.objects.filter(email=data.email).exist():
            NewsletterUser.objects.filter(email=data.email).delete()
            messages.success(request, 'Your email has been removed', "alert alert-success alert-dismissible")
        else:
            messages.warning(request, 'Your email does not exist', "alert alert-warning alert-dismissible")
    context = {
        'form': form,
    }
    template = "unsubscribe/unsubscribe.html"
    return render(request, template, context)
        