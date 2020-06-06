from django.urls import path
from . import views

urlpatterns = [
      path('search/', views.search, name='search'),
      path('news/<str:slug>', views.news_detail, name='newsInfo'),
      path('news/<str:slug>/<str:comment_id>/delete', views.comment_delete, name='comment-delete'),
      path('news/create/', views.news_create, name='news-create'),
      path('news/<str:slug>/update/', views.news_update, name='news-update'),
      path('news/<str:slug>/delete/', views.news_delete, name='news-delete'),
]
