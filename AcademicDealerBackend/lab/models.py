from django.db import models
from users.models import UserAccount, LoginFail

class LabInfo(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    create_date = models.DateTimeField()
    modified_date = models.DateTimeField()
    description = models.TextField()

class LabComment(models.Model):
    lab = models.ForeignKey(LabInfo, on_delete=models.CASCADE)
    owner = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    create_date = models.DateTimeField()
    modified_date = models.DateTimeField()
    description = models.TextField()
