from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required

from .models import Topic, Project, Reply

class IndexView(generic.ListView):
    template_name = 'projectinfo/index.html'
    context_object_name = 'topic_list'

    def get_queryset(self):
        return Topic.objects.order_by('-pub_date')

class TopicView(generic.DetailView):
    model = Topic
    template_name = 'projectinfo/topic.html'
    pk_url_kwarg = 'topic_id'

class ProjectView(generic.DetailView):
    model = Project
    template_name = 'projectinfo/project.html'
    pk_url_kwarg = 'project_id'