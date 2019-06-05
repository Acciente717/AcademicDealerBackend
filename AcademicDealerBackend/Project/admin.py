from django.contrib import admin
from .models import ProjectInfo, ProjectMember, ProjectComment

admin.site.register(ProjectInfo)
admin.site.register(ProjectMember)
admin.site.register(ProjectComment)
