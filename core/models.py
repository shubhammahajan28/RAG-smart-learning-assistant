from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class StudyResults(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    domain = models.CharField(max_length=100)
    topic = models.CharField(max_length=100)
    correctness = models.FloatField()
    time_spent = models.FloatField()
    confused = models.FloatField()
    weakness_score = models.FloatField()

class StudyRecord(models.Model):
    user_id = models.IntegerField(default=0)
    domain = models.CharField(max_length=100)
    topic = models.CharField(max_length=200)
    correctness = models.FloatField()
    time_spent = models.FloatField()
    confused = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.topic} ({self.domain})"