from django.db import models

# Create your models here.

class Records(models.Model):
    record_text = models.CharField(max_length=200)
    def __str__(self):
        return self.record_text
