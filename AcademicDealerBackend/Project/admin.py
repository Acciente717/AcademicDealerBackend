from django.contrib import admin

from .models import ProjectInfo, ProjectMember

admin.site.register(ProjectInfo)
admin.site.register(ProjectMember)
