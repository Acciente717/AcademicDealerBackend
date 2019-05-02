from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required

from .models import Topic, Project, Reply
from .forms import ProjectForm

class IndexView(generic.ListView):
    template_name = 'projectinfo/index.html'
    context_object_name = 'topic_list'

    def get_queryset(self):
        return Topic.objects.order_by('created_date')

class TopicDisplayView(generic.DetailView):
    model = Topic
    template_name = 'projectinfo/topic.html'
    pk_url_kwarg = 'topic_id'

    class Meta:
        ordering = ['modified_date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ProjectForm()
        return context

class ProjectView(generic.DetailView):
    model = Project
    template_name = 'projectinfo/project.html'
    pk_url_kwarg = 'project_id'

    class Meta:
        ordering = ['modified_date']

class TopicCreateProjectView(generic.CreateView):
    model = Topic
    form_class = ProjectForm
    pk_url_kwarg = 'topic_id'
    template_name = 'projectinfo/create_project.html'

    # def form_valid(self, form):
    #     form.instance.topic_id = Topic.objects.get(id = self.kwargs.get('topic_id'))
    #     return super(CreateProjectView, self).form_valid(form)
    
    def post(self, request, *args, **kwargs):
        # if not request.user.is_authenticated:
        #     return HttpResponseForbidden()
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('project', kwargs={'topic_id': self.object.topic_id_id, 'project_id':self.object.id})

class TopicDetail(generic.View):
    def get(self, request, *args, **kwargs):
        view = TopicDisplayView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = TopicCreateProjectView.as_view()
        return view(request, *args, **kwargs)