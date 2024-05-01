from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Workout

def home(request):
    context = {
        'workouts': Workout.objects.all()
    }
    return render(request, 'main/home.html', context)

class WorkoutListView(ListView):
    model = Workout
    template_name = 'main/home.html'
    context_object_name = 'workouts'
    ordering = ['-created_at']

class WorkoutDetailView(DetailView):
    model = Workout
    

def about(request):
    return render(request, 'main/about.html')