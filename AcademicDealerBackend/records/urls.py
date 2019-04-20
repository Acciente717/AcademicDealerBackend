from django.urls import path

from . import views

app_name = 'records'

urlpatterns = [
    path('', views.detail, name='detail'),
    path('delete/', views.delete, name='delete'),
    path('insert/', views.insert, name='insert')
]
