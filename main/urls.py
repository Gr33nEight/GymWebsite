from django.urls import path
from .views import WorkoutListView, WorkoutDetailView, MyWorkoutsListView
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', WorkoutListView.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('calculator-bmi/', views.calculatorBmi, name='calculator-bmi'),
    path('calculator-calories/', views.calculatorCalories, name='calculator-calories'),
    path('my-workouts/', login_required(MyWorkoutsListView.as_view()), name='my-workouts'),
    path('workout/<int:pk>/', WorkoutDetailView.as_view(), name='workout-detail'),
    path('import-workouts/', views.import_workouts, name='import_workouts'),
    path('export-workouts/', views.export_workouts, name='export_workouts'),
    path('add-workout/', views.add_workout, name='add_workout'),
    path('delete-workout/', views.delete_workout, name='delete_workout')
]