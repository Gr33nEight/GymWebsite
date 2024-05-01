from django.urls import path
from .views import WorkoutListView, WorkoutDetailView
from . import views

urlpatterns = [
    path('', WorkoutListView.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('workout/<int:pk>/', WorkoutDetailView.as_view(), name='workout-detail'),
]