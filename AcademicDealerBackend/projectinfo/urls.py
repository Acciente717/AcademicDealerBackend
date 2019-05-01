from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:topic_id>/', views.TopicView.as_view(), name='topic'),
    path('<int:topic_id>/<int:project_id>', views.ProjectView.as_view(), name='project'),
    # path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # path('<int:question_id>/vote/', views.vote, name='vote'),
]