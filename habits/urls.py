from django.urls import path

from habits.views import HabitCreateAPIView, HabitListAPIView, HabitRetrieveAPIView, HabitUpdateAPIView, \
    HabitDestroyAPIView, MyHabitListAPIView

app_name ='habits'

urlpatterns = [
    path('habit/create/', HabitCreateAPIView.as_view(), name='habit_create'),
    path('habits/publish/', HabitListAPIView.as_view(), name='habits_list'),
    path('habits/', MyHabitListAPIView.as_view(), name='my_habits_list'),
    path('habit/<int:pk>/', HabitRetrieveAPIView.as_view(), name='habit_detail'),
    path('habit/update/<int:pk>/', HabitUpdateAPIView.as_view(), name='habit_update'),
    path('habit/delete/<int:pk>/', HabitDestroyAPIView.as_view(), name='habit_delete'),
]
