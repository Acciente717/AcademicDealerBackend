from django.urls import path
from . import views

# app_name = 'users'

urlpatterns = [
    path('create/', views.create, name='create'),
    # path('edit/', views.edit, name='edit'),
    # path('view/', views.view, name='view'),
    # path('delete/', views.delete, name='delete'),
    # path('join/', views.join, name='join')
    # path('drop/', views.drop, name='drop')
]
