from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .decorators import unauthenticated_user, allowed_users
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
# Create your views here.



def newsletter_subscribe(request):
    if request.method == "POST":
        form = NewsletterUserSignUpForm(request.POST or None)
        
        if form.is_valid():
            data = form.save(commit=False)
            if NewsletterUser.objects.filter(email=data.email).exists():
                messages.warning(request, 'Email Already Exists', "alert alert-warning alert-dismissible")
            else:
                data.save()
                messages.success(request, 'Your Email has been submitted', "alert alert-success alert-dismissible")
                template = render_to_string('newsletters/subscribe_email.html')
                send_mail(
                    "Thank You for Joining Our Newsletter",
                    template,
                    settings.EMAIL_HOST_USER,
                    [data.email],
                    fail_silently=False
                )
    else:
        form = NewsletterUserSignUpForm(request.POST or None)
    context = {
        'form': form,
    }
    template = "newsletters/subscribe.html"
    return render(request, template, context)

def newsletter_unsubscribe(request):
    if request.method == "POST":
        form = NewsletterUserSignUpForm(request.POST or None)
        
        if form.is_valid():
            data = form.save(commit=False)
            if NewsletterUser.objects.filter(email=data.email).exists():
                NewsletterUser.objects.filter(email=data.email).delete()
                messages.success(request, 'Your email has been removed', "alert alert-success alert-dismissible")
                template = render_to_string('newsletters/unsubscribe_email.html')
                send_mail(
                    "Thank You for Joining Our Newsletter",
                    template,
                    settings.EMAIL_HOST_USER,
                    [data.email],
                    fail_silently=False
                )
            else:
                messages.warning(request, 'Your email does not exist', "alert alert-warning alert-dismissible")
    else:
        form = NewsletterUserSignUpForm(request.POST or None)
                
    context = {
        'form': form,
    }
    template = "newsletters/unsubscribe.html"
    return render(request, template, context)

@allowed_users(allowed_roles=['Admin'])
def control_newsletter(request):
    if request.method == "POST":
        form = NewsletterCreationForm(request.POST or None)
        if form.is_valid():
            data = form.save()
            newsletter = Newsletter.objects.get(id=data.id)
        
            if newsletter.status == 'Published':
                subject = newsletter.subject
                body = newsletter.body
                from_email = settings.EMAIL_HOST_USER
                for email in newsletter.email.all():
                    send_mail(
                        subject=subject,
                        from_email=from_email,
                        recipient_list=[email],
                        message=body, 
                        fail_silently=False
                    )
            return redirect('control_newsletter')
        
    else:
        form = NewsletterCreationForm(request.POST or None)
                
    context = {
        'form': form
    }
    template = "controlpanels/control_newsletter.html"
    return render(request, template, context)


@allowed_users(allowed_roles=['Admin'])
def control_newsletter_list(request):
    newsletters = Newsletter.objects.all()
    paginator = Paginator(newsletters, 10)
    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)    
    
    index = queryset.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 5 if index >= 5 else 0
    end_index = index + 5 if index <= max_index -5 else max_index
    page_range = paginator.page_range[start_index:end_index]
    
    context = {
        'queryset': queryset,
        'page_range': page_range,
    }
    template = "controlpanels/control_newsletter_list.html"
    return render(request, template, context)


@allowed_users(allowed_roles=['Admin'])
def control_newsletter_detail(request, pk):
    newsletter = get_object_or_404(Newsletter, pk=pk)
    
    context = {
        'newsletter': newsletter
    }
    template = "controlpanels/control_newsletter_detail.html"
    return render(request, template, context)


@allowed_users(allowed_roles=['Admin'])
def control_newsletter_edit(request, pk):
    newsletter = get_object_or_404(Newsletter, pk=pk)
    
    if request.method == "POST":
        form = NewsletterCreationForm(request.POST, instance=newsletter)
        
        if form.is_valid():
            newsletter = form.save()
            
            if newsletter.status == 'Published':
                subject = newsletter.subject
                body = newsletter.body
                from_email = settings.EMAIL_HOST_USER
                for email in newsletter.email.all():
                    send_mail(
                        subject=subject,
                        from_email=from_email,
                        recipient_list=[email],
                        message=body, 
                        fail_silently=False
                    )
            return redirect('control_newsletter_detail', pk=newsletter.pk)
        
    else:
        form = NewsletterCreationForm(instance=newsletter)

    context = {
        'form': form
    }
    template = "controlpanels/control_newsletter.html"
    return render(request, template, context)


@allowed_users(allowed_roles=['Admin'])
def control_newsletter_delete(request, pk):
    newsletter = get_object_or_404(Newsletter, pk=pk)
    newsletter.delete()
    return redirect('control_newsletter_list')