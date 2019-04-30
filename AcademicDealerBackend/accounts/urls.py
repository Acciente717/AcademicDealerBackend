from django.urls import include, path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),    
    path('signup/', views.SignUp.as_view(), name='signup'),
]
