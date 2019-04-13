from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('polls/', include('polls.urls')),
    path('ResponseTest/', include('ResponseTest.urls')),
    path('admin/', admin.site.urls),
]


