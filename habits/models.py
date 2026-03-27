from django.db import models
from django.utils import timezone

from users.models import CustomUser


class Wont(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Создатель")
    place = models.CharField(max_length=100, verbose_name="Место")
    time = models.TimeField(verbose_name="Время выполнения")
    action = models.CharField(max_length=100, verbose_name="Действие")
    is_pleasant = models.BooleanField(default=True, verbose_name="Признак приятной привычки")
    connection_wont = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Связанная привычка")
    period = models.PositiveIntegerField(default=7, verbose_name='Кол-во выполнений в неделю')
    reward = models.CharField(max_length=100, null=True, blank=True, verbose_name="Вознаграждение")
    time_to_action = models.DurationField(default=timezone.timedelta(seconds=60), verbose_name="Время на выполнения")
    is_published = models.BooleanField(default=True, verbose_name="Признак публичности")

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"

    def __str__(self):
        return {self.action}