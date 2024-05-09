from django.urls import path
from .views import WorkoutListView, WorkoutDetailView, MyWorkoutListView
from . import views

urlpatterns = [
    path('', WorkoutListView.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('calculator-bmi/', views.calculatorBmi, name='calculator-bmi'),
    path('calculator-calories/', views.calculatorCalories, name='calculator-calories'),
    path('my-workouts/', MyWorkoutListView.as_view(), name='my-workouts'),
    path('workout/<int:pk>/', WorkoutDetailView.as_view(), name='workout-detail'),
]