from django.urls import path

from apps.core import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about_project, name='about_project'),
    path('books/', views.books, name='books'),
    path('authors/', views.authors, name='authors'),
    path('readers/', views.readers, name='readers'),
    path('genres/', views.genres, name='genres'),
    path('publishing/', views.publishing, name='publishing'),
    path('lend/', views.lend_page, name='lend')
]