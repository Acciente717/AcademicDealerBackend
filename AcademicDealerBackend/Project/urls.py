from django.urls import path
from . import views

# app_name = 'users'

urlpatterns = [
    path('<url_action>/', views.api_dispatch, name='api_dispatch'),
    path('comment/create/', views.comment_create, name='comment_create'),
    path('comment/edit/', views.comment_edit, name='comment_edit'),
    path('comment/delete/', views.comment_delete, name='comment_delete'),
    path('comment/view/', views.comment_view, name='comment_view')
]
