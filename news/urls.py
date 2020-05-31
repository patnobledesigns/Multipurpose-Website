from django.urls import path
from . import views

urlpatterns = [
      path('search/', views.search, name='search'),
      path('news/<str:pk>', views.news_detail, name='newsInfo'),
      path('news/create/', views.news_create, name='news-create'),
      path('news/<str:pk>/update/', views.news_update, name='news-update'),
      path('news/<str:pk>/delete/', views.news_delete, name='news-delete'),
]
