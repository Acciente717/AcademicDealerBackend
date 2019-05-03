from django.http import HttpResponseRedirect
from django.http import Http404
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .forms import ProjectForm, ReplyForm
from .models import Topic, Project, Reply

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

@method_decorator(login_required, name='dispatch')
class TopicCreateProjectView(generic.CreateView):
    model = Project
    form_class = ProjectForm
    pk_url_kwarg = 'topic_id'

    def form_valid(self, form):
        form.instance.topic = Topic.objects.get(id = self.kwargs.get('topic_id'))
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('project', kwargs={'topic_id': self.object.topic_id, 'project_id':self.object.id})

class TopicDetail(generic.View):
    def get(self, request, *args, **kwargs):
        view = TopicDisplayView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = TopicCreateProjectView.as_view()
        return view(request, *args, **kwargs)

class ProjectDisplayView(generic.DetailView):
    model = Project
    template_name = 'projectinfo/project.html'
    pk_url_kwarg = 'project_id'

    class Meta:
        ordering = ['modified_date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ReplyForm()
        return context

@method_decorator(login_required, name='dispatch')
class ProjectCreateProjectView(generic.CreateView):
    model = Reply
    form_class = ReplyForm
    pk_url_kwarg = 'project_id'

    def form_valid(self, form):
        form.instance.project = Project.objects.get(id = self.kwargs.get('project_id'))
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        project = self.object.project
        return reverse('project', kwargs={'topic_id': project.topic.id, 'project_id': project.id})

class ProjectView(generic.DetailView):
    def get(self, request, *args, **kwargs):
        # first check for url
        topic_id = kwargs['topic_id']
        project_id = kwargs['project_id']

        if Project.objects.get(id=project_id).topic.id != topic_id:
            raise Http404("Not found")

        view = ProjectDisplayView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = ProjectCreateProjectView.as_view()
        return view(request, *args, **kwargs)