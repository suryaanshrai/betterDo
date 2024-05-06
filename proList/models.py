from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

# Create your models here.
class User(AbstractUser):
    pass

class Task(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    task=models.CharField(max_length=256)
    start_time=models.DateTimeField(blank=True,default=timezone.now())
    end_time=models.DateTimeField(blank=True, null=True)
    group=models.CharField(max_length=256,blank=True,null=True)

    def __str__(self):
        return f"{self.user} started {self.task} at {self.start_time}"


class Remark(models.Model):
    task=models.ForeignKey(Task, on_delete=models.CASCADE, related_name="remark")
    remark=models.TextField()

    def __str__(self):
        return f"{self.task}:{self.remark}"
    
class Reminder(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE,related_name="reminders")
    reminder=models.CharField(max_length=256)

    def __str__(self):
        return f"{self.user} needs to reminded about {self.reminder}"