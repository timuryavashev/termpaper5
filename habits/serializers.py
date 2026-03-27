from rest_framework import serializers
from rest_framework.serializers import ValidationError

from habits.models import Habit
from habits.validators import HabitDurationValidator, MutualExclusionsValidator, HabitPeriodValidator


class HabitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ['user']
        validators = [
            HabitDurationValidator('time_to_action'),
            HabitPeriodValidator('period'),
            MutualExclusionsValidator(fields=['reward', 'connection_wont'])
        ]


    def validate(self, attrs):

        if attrs.get('is_pleasant'):
            if attrs.get('reward') or attrs.get('connection_wont'):
                raise ValidationError('У приятной привычки не может быть вознаграждения или связанной привычки.')

        if attrs.get('connection_wont'):
            pk = attrs.get('connection_wont').id
            wont = Habit.objects.filter(pk=pk).first()
            if not wont.is_pleasant:
                raise ValidationError('В связанные привычки могут попадать только привычки с признаком приятной привычки.')

        return attrs