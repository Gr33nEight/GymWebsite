from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Workout
from django.db import models

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

class MyWorkoutListView(ListView):
    model = Workout
    template_name = 'main/my-workouts.html'
    context_object_name = 'myWorkouts'
    ordering = ['-created_at']

class WorkoutDetailView(DetailView):
    model = Workout
    
def about(request):
    return render(request, 'main/about.html')

def get_bmi_category(bmi):
    match bmi:
        case _ if bmi < 18.5:
            return "Niedowaga"
        case _ if 18.5 <= bmi < 25:
            return "Prawidłowa waga"
        case _ if 25 <= bmi < 30:
            return "Nadwaga"
        case _:
            return "Otyłość"


def calculatorBmi(request):
    bmi = 0

    if request.method == 'POST':
        weight = request.POST.get('weight')
        height = request.POST.get('height')
        
        if weight and height:
            try:
                heightToMeters = int(height)/100
                bmi = int(weight) / (heightToMeters*heightToMeters)  
            except ValueError:
                pass  

    context = {
        'bmi' : round(bmi, 2),
        'description': get_bmi_category(bmi)
    }

    return render(request, 'main/calculator-bmi.html', context)


def calculatorCalories(request):
    calories = 0
    protein = 0
    bmi = 0
    activity = 1.2

    if request.method == 'POST':
        age = int(request.POST.get('age'))
        training = int(request.POST.get('training'))
        user_profile = request.user.profile

        if age and training:
            try:
                bmi = user_profile.bmi_count
                if training >= 3 and training < 5:
                    activity = 1.5
                elif training >= 5:
                    activity = 1.8
                calories = ((10 * bmi) + (6.25 * age) + 5) * activity
                protein = 1.5 * bmi

            except ValueError:
                pass    

    context = {
        'calories' : calories,
        'protein' : protein
    }   

    return render(request, 'main/calculator-calories.html', context)