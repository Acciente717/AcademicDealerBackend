from django.urls import path
from . import views

# app_name = 'users'

urlpatterns = [
    path('create/', views.create, name='create'),
    path('edit/', views.edit, name='edit'),
    path('delete/', views.delete, name='delete'),
    path('view/', views.view, name='view'),
    path('join/', views.join, name='join'),
    path('drop/', views.drop, name='drop'),
    path('search/', views.search, name='search')
]
