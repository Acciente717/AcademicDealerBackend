from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('project/', include('Project.urls')),
    path('seminar/', include('seminar.urls')),
    path('lab/', include('lab.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
]