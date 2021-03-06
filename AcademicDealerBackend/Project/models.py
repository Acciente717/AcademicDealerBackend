from django.db import models
from users.models import UserAccount, LoginFail

class ProjectInfo(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    create_date = models.DateTimeField()
    modified_date = models.DateTimeField()
    member_total_need = models.PositiveIntegerField()
    description = models.TextField()

class ProjectMember(models.Model):
    project = models.ForeignKey(ProjectInfo, on_delete=models.CASCADE)
    person = models.ForeignKey(UserAccount, on_delete=models.CASCADE)

class ProjectComment(models.Model):
    project = models.ForeignKey(ProjectInfo, on_delete=models.CASCADE)
    owner = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    create_date = models.DateTimeField()
    modified_date = models.DateTimeField()
    description = models.TextField()
