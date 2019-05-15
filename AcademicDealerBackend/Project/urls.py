from django.urls import path
from . import views

# app_name = 'users'

urlpatterns = [
    path('<url_action>/', views.api_dispatch, name='api_dispatch'),
    path('comment/<url_action>/', views.comment_api_dispatch, name='comment_api_dispatch')
]
