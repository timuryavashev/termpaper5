from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from habits.models import Habit
from habits.paginators import HabitPaginator
from habits.permissions import IsOwner
from habits.serializers import HabitSerializer


class HabitCreateAPIView(generics.CreateAPIView):

    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HabitRetrieveAPIView(generics.RetrieveAPIView):

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class HabitListAPIView(generics.ListAPIView):

    serializer_class = HabitSerializer
    queryset = Habit.objects.filter(is_published=True)
    permission_classes = [IsAuthenticated]
    pagination_class = HabitPaginator


class MyHabitListAPIView(generics.ListAPIView):

    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = HabitPaginator

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)


class HabitUpdateAPIView(generics.UpdateAPIView):

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class HabitDestroyAPIView(generics.DestroyAPIView):

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]

