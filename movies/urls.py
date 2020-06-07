from django.urls import path
from . import views
from .views import Home, Movies

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('search-result/', views.search_home, name='searchresult'),
    path('movies/', Movies.as_view(), name='allmovies'),
    path('movies/<str:slug>/', views.movies_detail, name='allmoviesInfo'),
    path('movies/edit-review/<str:slug>/<int:pk>/', views.edit_review, name='editreview'),
    path('movies/delete-review/<str:slug>/<int:pk>/', views.delete_review, name='deletereview'),
    path('movies/create-movie/', views.create_movie, name='createmovie'),
    path('movies/update-movie/<str:slug>', views.update_movie, name='updatemovie'),
    path('movies/delete-movie/<str:slug>', views.delete_movie, name='deletemovie'),
]
