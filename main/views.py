from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Workout, User, Workout_Exercise, Body_Part
from import_export import resources
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
import csv

class WorkoutListView(ListView):
    model = Workout
    template_name = 'main/home.html'
    context_object_name = 'workouts'
    ordering = ['-created_at']

class MyWorkoutsListView(ListView):
    model = Workout
    template_name = 'main/my-workouts.html'
    context_object_name = 'workouts'
    
    def get_queryset(self):
        return self.request.user.profile.users_workouts.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['myWorkouts'] = self.request.user.profile.users_workouts.all()
        return context

class WorkoutDetailView(DetailView):
    model = Workout

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user.profile

        workout = self.get_object()        
        context['current_user'] = current_user

        return context
    
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


def calculatedBMI(request):
    weight = request.POST.get('weight') 
    height = request.POST.get('height')
    if weight and height:
        try:
            heightToMeters = int(height) / 100
            return int(weight) / (heightToMeters * heightToMeters)
        except ValueError:
            return 0
    else:
        return 0

def saveBMI(request, bmi):
    profile = request.user.profile
    profile.bmi_count = bmi
    profile.save()

def calculatorBmi(request):
    bmi = 0
    
    if request.method == 'POST':
        bmi = calculatedBMI(request)
        saveBMI(request, bmi)

    context = {
        'bmi': round(bmi, 2),
        'description': get_bmi_category(calculatedBMI(request)),
    }

    return render(request, 'main/calculator-bmi.html', context)

@login_required
def calculatorCalories(request):
    daily_calories = 0
    if request.method == 'POST':
        try:
            gender = str(request.POST.get('gander', ''))
            age = int(request.POST.get('age', ''))
            weight = float(request.POST.get('weight', ''))
            height = float(request.POST.get('height', ''))
            activity_level = str(request.POST.get('activity_level', ''))
            diet_goal = str(request.POST.get('diet_goal', ''))

            # Sprawdź czy wszystkie pola zostały wypełnione
            if not all([gender, age, weight, height, activity_level, diet_goal]):
                raise ValueError("Wszystkie pola są wymagane")

            # Wzór na BMR 
            if gender.lower() == 'male':
                bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
            elif gender.lower() == 'female':
                bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
            else:
                raise ValueError("Twoja płeć musi być: 'male' lub 'female'")

            # Poziom aktywności
            activity_factors = {
                'nieaktywny': 1.2,
                'lekko-aktywny': 1.375,
                'srednio-aktywny': 1.55,
                'aktywny': 1.725,
                'bardzo-aktywny': 1.9
            }
            
            if activity_level.lower() not in activity_factors:
                raise ValueError("Poziom twojej aktywności musi być: 'nieaktywny', 'lekko aktywny', 'średnio aktywny', 'aktywny', 'bardzo aktywny'")
            
            daily_calories = bmr * activity_factors[activity_level.lower()]

            # Cel diety
            if diet_goal.lower() == 'utrzymanie':
                pass  
            elif diet_goal.lower() == 'chudniecie':
                daily_calories -= 500 
            elif diet_goal.lower() == 'przytycie':
                daily_calories += 500  
            else:
                raise ValueError("Twój cel diety musi być: 'utrzymanie', 'chudnięcie', lub 'przytycie'")

        except ValueError as e:
            messages.error(request, f'Muszisz wypełnić wszystkie pola!')
            return render(request, 'main/calculator-calories.html', {'calories':0})

    context = {
        'calories' : int(daily_calories)
    }   

    return render(request, 'main/calculator-calories.html', context)


class WorkoutResource(resources.ModelResource):
    class Meta:
        model = Workout


def export_workouts(request):
    try:
        profile = request.user.profile
        users_workouts = profile.users_workouts.all()
        workout_resource = WorkoutResource()
        dataset = workout_resource.export(queryset=users_workouts)
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="workouts.csv"'

        writer = csv.writer(response)
        writer.writerow(dataset.headers)
        for row in dataset:
            writer.writerow(row)

        return response
    except Exception as e:
        messages.error(request, f'Wystąpił błąd podczas eksportu treningów: {e}')
        return redirect('my-workouts')

def import_workouts(request):
    if request.method == 'POST':
        try:
            csv_file = request.FILES['myfile']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.reader(decoded_file)

            next(reader)
            for data in reader:
                id = data[0]
                title = data[1]
                description = data[2]
                created_at = data[3]
                author_id = data[4]
                bmi_count = data[5]
                body_parts_ids = data[6].split(',') if data[6] else []
                workout_exercises_ids = data[7].split(',') if data[7] else []

                author = User.objects.get(id=author_id)
                body_parts = Body_Part.objects.filter(id__in=body_parts_ids)
                workout_exercises = Workout_Exercise.objects.filter(id__in=workout_exercises_ids)

                workout = Workout(
                    id=id,
                    title=title,
                    description=description,
                    created_at=created_at,
                    author=author,
                    bmi_count=bmi_count
                )

                workout.body_parts.set(body_parts) 
                workout.workout_exercises.set(workout_exercises)

                request.user.profile.users_workouts.add(workout)

            messages.success(request, f'Twoje treningi zostały poprawnie zaimportowane')
        except Exception as e:
            print(f"An error occurred while processing the file: {e}")
            messages.error(request, f'Niestety nie udało się zaimportować twoich treningów. Upewnij się, że wybrany plik jest prawidłowym plikiem CSV.')

        return redirect('my-workouts')
    return redirect('my-workouts')

def add_workout(request):
    if request.method == "POST":
        try:
            workout_id = request.POST.get('workout_id')
            workout = Workout.objects.get(id=workout_id)
            request.user.profile.users_workouts.add(workout)
            messages.success(request, f'Trening został dodany do zakładki "Moje treningi"')
        except Exception as e:
            print(f"An error occurred: {e}")
            messages.error(request, f'Niestety nie udało się dodać do twoich treningów. Spróbuj ponownie później.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def delete_workout(request):
    if request.method == "POST":
        try:
            workout_id = request.POST.get('workout_id')
            workout = Workout.objects.get(id=workout_id)
            request.user.profile.users_workouts.remove(workout)
            messages.success(request, f'Trening został usunięty z zakładki "Moje treningi"')
        except Exception as e:
            print(f"An error occurred: {e}")
            messages.error(request, f'Niestety nie udało się usunąć z twoich treningów. Spróbuj ponownie później.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))