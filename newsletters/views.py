from django.shortcuts import render
from .models import NewsletterUser
from .forms import NewsletterUserSignUpForm

# Create your views here.

def newsletter_subscribe(request):
    form = NewsletterUserSignUpForm(request.POST or None)
    
    if form.is_valid():
        data = form.save(commit=False)
        if NewsletterUser.objects.filter(email=data.email).exist():
            print('User Already Exist')
        else:
            data.save()
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
        else:
            print('Sorry but we did not find your email address')
    context = {
        'form': form,
    }
    template = "unsubscribe/unsubscribe.html"
    return render(request, template, context)
        