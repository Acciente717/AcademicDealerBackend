from django.db import models
from users.models import UserAccount, LoginFail

class LabInfo(models.Model):
    name = models.CharField(max_length=255)
    school = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    owner = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=31)
    front_page_url = models.URLField()
    pic_url = models.URLField()
    logo_url = models.URLField()
    supervisors = models.TextField()
    create_date = models.DateTimeField()
    modified_date = models.DateTimeField()
    description = models.TextField()

class LabComment(models.Model):
    lab = models.ForeignKey(LabInfo, on_delete=models.CASCADE)
    owner = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    create_date = models.DateTimeField()
    modified_date = models.DateTimeField()
    description = models.TextField()
