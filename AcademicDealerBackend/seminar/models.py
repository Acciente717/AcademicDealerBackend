from django.db import models
from users.models import UserAccount, LoginFail

class SeminarInfo(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    create_date = models.DateTimeField()
    modified_date = models.DateTimeField()
    member_number_limit = models.PositiveIntegerField()
    description = models.TextField()

class SeminarMember(models.Model):
    seminar = models.ForeignKey(SeminarInfo, on_delete=models.CASCADE)
    person = models.ForeignKey(UserAccount, on_delete=models.CASCADE)

class SeminarComment(models.Model):
    seminar = models.ForeignKey(SeminarInfo, on_delete=models.CASCADE)
    owner = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    create_date = models.DateTimeField()
    modified_date = models.DateTimeField()
    description = models.TextField()
