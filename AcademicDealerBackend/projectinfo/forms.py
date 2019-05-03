from django import forms
from django.forms import ModelForm
from .models import Topic, Project, Reply

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'text']

class ReplyForm(ModelForm):
    class Meta:
        model = Reply
        fields = ['text']