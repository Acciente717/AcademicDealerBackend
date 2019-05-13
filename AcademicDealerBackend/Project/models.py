from django.db import models
from users.models import UserAccount

class ProjectInfo(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    member_total_need = models.PositiveIntegerField()
    description = models.TextField()

class ProjectMember(models.Model):
    project = models.ForeignKey(ProjectInfo, on_delete=models.CASCADE)
    person = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
