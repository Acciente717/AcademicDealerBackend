from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('view/', views.view, name='view'),
    path('edit/', views.edit, name='edit'),
    path('delete/', views.delete, name='delete'),
    path('follow/', views.follow, name='follow')
    # path('unfollow/', views.unfollow, name='unfollow')
]
