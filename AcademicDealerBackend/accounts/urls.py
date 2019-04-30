from django.urls import include, path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from . import views

urlpatterns = [
    # path('login/', auth_views.LoginView.as_view(),name='login'),
    # path('logout/', auth_views.LogoutView.as_view(),name='logout'),
    # path('password_reset/', auth_views.PasswordResetView.as_view(success_url=reverse_lazy('password_reset_done'))),
    # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('password_reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    path('', include('django.contrib.auth.urls')),
    
    path('signup/', views.SignUp.as_view(), name='signup'),
]
