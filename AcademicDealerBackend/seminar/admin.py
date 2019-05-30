from django.contrib import admin
from .models import SeminarInfo, SeminarMember, SeminarComment

admin.site.register(SeminarInfo)
admin.site.register(SeminarMember)
admin.site.register(SeminarComment)
