from django.urls import path
from newsletters.views import control_newsletter, control_newsletter_list, control_newsletter_detail, control_newsletter_edit, control_newsletter_delete, user_settings

urlpatterns = [
     path('control_settings/', user_settings, name='control_settings'),
     path('newsletter/', control_newsletter, name='control_newsletter'),
     path('newsletter-list/', control_newsletter_list, name='control_newsletter_list'),
     path('newsletter/<str:pk>/', control_newsletter_detail, name='control_newsletter_detail'),
     path('newsletter/<str:pk>/edit', control_newsletter_edit, name='control_newsletter_edit'),
     path('newsletter/<str:pk>/delete', control_newsletter_delete, name='control_newsletter_delete'),
]
