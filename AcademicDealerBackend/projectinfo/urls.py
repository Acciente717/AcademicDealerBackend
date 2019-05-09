from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:topic_id>/', views.TopicDetail.as_view(), name='topic'),
    path('<int:topic_id>/<int:project_id>', views.ProjectView.as_view(), name='project'),
]