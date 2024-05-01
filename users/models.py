from django.db import models
from django.contrib.auth.models import User
from main.models import Workout
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bmi_count = models.IntegerField(null=True)
    created_at = models.DateTimeField(default=timezone.now)
    users_workouts = models.ManyToManyField(Workout, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'