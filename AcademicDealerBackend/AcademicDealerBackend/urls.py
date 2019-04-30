from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import TemplateView # new


urlpatterns = [
    path('records/', include('records.urls')),
    path('polls/', include('polls.urls')),
    path('ResponseTest/', include('ResponseTest.urls')),
    path('accounts/', include('accounts.urls', namespace="accounts")),
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),

]


