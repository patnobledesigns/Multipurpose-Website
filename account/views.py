from django.shortcuts import render, redirect, reverse, Http404
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:    
        if request.method == "POST":
            form = CreateUserForm(request.POST or None)
            if form.is_valid():
                user = form.save(commit=False)
                password = form.cleaned_data.get('password1')
                user.set_password(password)
                user.save()
                new_user = authenticate(username=user.username, password=password)
                
                login(request, new_user)
                return redirect('/')
                
        else:     
            form = CreateUserForm(request.POST or None)         
   
    context={
        'title': 'Register',
        'form': form
    }
    
    return render(request, 'account/register.html', context)


def loginpage(request):
    # login Validation
    if request.user.is_authenticated:
        return redirect('home')
    else:    
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:  
                    login(request, user)
                    if 'next' in request.POST:
                        return redirect(request.POST.get('next'))
                    else:
                        return redirect('home')
                else:
                    messages.info(request, 'Your account has been disabled.')
            else:
                messages.info(request, 'Username Or Password is Incorrect')              
    context = {
        'title': 'Login'
    }
    return render(request, 'account/login.html', context)
    
           
def logoutpage(request):      
    logout(request)
    return redirect('home')


@login_required(login_url='login')
def userProfile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUdateForm(request.POST, 
                                  request.FILES, 
                                        instance=request.user.author)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUdateForm(instance=request.user.author)
        
    context  = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'account/profile.html', context)

    

