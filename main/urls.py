from django.urls import path
from .views import WorkoutListView, WorkoutDetailView, MyWorkoutListView
from . import views

urlpatterns = [
    path('', WorkoutListView.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('calculator/', views.calculator, name='calculator'),
    path('my-workouts/', MyWorkoutListView.as_view(), name='my-workouts'),
    path('workout/<int:pk>/', WorkoutDetailView.as_view(), name='workout-detail'),
]