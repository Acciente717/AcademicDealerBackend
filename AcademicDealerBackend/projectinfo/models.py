from django.db import models
from django.utils import timezone
from django.conf import settings
from datetime import datetime

class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
    
    def update_modify_time(self):
        modified_date = datetime.now()
        self.save()

class Topic(BaseModel):
    topic_text = models.CharField(max_length=200)

class Project(BaseModel):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField(max_length=20000)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Reply(BaseModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    text = models.TextField(max_length=20000)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
