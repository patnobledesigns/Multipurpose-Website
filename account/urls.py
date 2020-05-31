from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.loginpage, name='login'),
    path('logout/', views.logoutpage, name='logout'),
    path('profile/', views.userProfile, name='profile'),
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(template_name='account/password_reset.html'), 
         name='password_reset'),
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='account/password_reset_done.html'), 
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset_done.html'), 
         name='password_reset_confirm'),
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'), 
         name='password_reset_complete'),
]
