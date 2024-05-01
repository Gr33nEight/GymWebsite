from django.contrib import admin
from .models import Workout, Body_Part, Exercise, Workout_Exercise

admin.site.register(Workout)
admin.site.register(Body_Part)
admin.site.register(Exercise)
admin.site.register(Workout_Exercise)

