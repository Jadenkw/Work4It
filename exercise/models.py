import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from embed_video.fields import EmbedVideoField

# Create your models here.



class Item(models.Model):
    video = EmbedVideoField()  # same like models.URLField()
    video_title = models.CharField(max_length=200, default="")
    def __str__(self):
        return self.video_title

class Workout(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    workout_title= models.CharField(max_length=200, default=timezone.now)
    workout_pub_date = models.DateTimeField()
    workout_start_time = models.TimeField(default = timezone.now)
    workout_end_time = models.TimeField(default = timezone.now)
    workout_description = models.TextField()
    workout_points = models.IntegerField(default=0)
    workout_calories = models.IntegerField(default=0)
    # total_points = models.IntegerField(default = 0)
    def __str__(self):
        return self.workout_title

