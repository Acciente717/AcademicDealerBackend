from django.contrib import admin

from .models import Topic, Project, Reply

admin.site.register(Topic)
admin.site.register(Project)
admin.site.register(Reply)
