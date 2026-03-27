from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    char_id = models.CharField(max_length=255, verbose_name="chat_id", null=True, blank=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
