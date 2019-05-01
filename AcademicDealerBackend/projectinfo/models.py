import datetime

from django.db import models
from django.utils import timezone

class Topic(models.Model):
    topic_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', auto_now=True)

class Project(models.Model):
    topic_id = models.ForeignKey(Topic, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField(max_length=20000)
    owner = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', auto_now=True)

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Reply(models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    text = models.TextField(max_length=20000)
    owner = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', auto_now=True)