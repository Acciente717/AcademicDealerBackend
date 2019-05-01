import datetime

from django.db import models
from django.utils import timezone

class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Topic(BaseModel):
    topic_text = models.CharField(max_length=200)

class Project(BaseModel):
    topic_id = models.ForeignKey(Topic, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField(max_length=20000)
    owner = models.CharField(max_length=200)

class Reply(BaseModel):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    text = models.TextField(max_length=20000)
    owner = models.CharField(max_length=200)