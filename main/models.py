from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import int_list_validator

class Body_Part(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Exercise(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    instructions = models.TextField()
    body_parts = models.ManyToManyField(Body_Part)

    def __str__(self):
        return self.title

class Workout_Exercise(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, default="")
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets_count = models.IntegerField(default=0)
    reps_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Workout(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    bmi_count = models.IntegerField()
    body_parts = models.ManyToManyField(Body_Part)
    workout_exercises = models.ManyToManyField(Workout_Exercise)

    def __str__(self):
        return self.title