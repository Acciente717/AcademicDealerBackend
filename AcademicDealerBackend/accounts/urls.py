from django.urls import include, path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'accounts'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('accounts/logout/', auth_views.LogoutView.as_view(redirect_field_name=None)),
]
