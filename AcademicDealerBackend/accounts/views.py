from django.shortcuts import render

from accounts.forms import MyUserCreationForm
from django.urls import reverse_lazy
from django.views import generic

class SignUp(generic.CreateView):
    form_class = MyUserCreationForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'registration/signup.html'
