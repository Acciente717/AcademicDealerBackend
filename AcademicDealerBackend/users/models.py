from django.db import models
import datetime

class UserAccount(models.Model):
    email = models.EmailField(max_length=254, unique=True) # 254 is correct
    pw_hash = models.CharField(max_length=255)
    create_time = models.DateTimeField(auto_now_add=True)
    last_activated_time = models.DateTimeField(default=datetime.date.today)

    real_name = models.CharField(max_length=255)
    nick_name = models.CharField(max_length=255, unique=True)
    pic_url = models.URLField(max_length=512)
    school = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    enrollment_date = models.DateField()
    profile = models.TextField()
