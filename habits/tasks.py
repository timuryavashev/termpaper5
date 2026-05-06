from celery import shared_task
from django.utils import timezone
from habits.models import Habit
from habits.services import send_telegram_message


@shared_task
def send_habit_reminders():
    now = timezone.localtime()
    current_time = now.time().replace(second=0, microsecond=0)

    # Ищем привычки, время которых совпадает с текущей минутой
    habits = Habit.objects.filter(
        time__hour=current_time.hour,
        time__minute=current_time.minute,
        user__tg_chat_id__isnull=False
    ).select_related('user')

    for habit in habits:
        text = (
            f"🔔 Напоминание о привычке!\n\n"
            f"Действие: {habit.action}\n"
            f"Место: {habit.place}\n"
            f"Время: {habit.time.strftime('%H:%M')}"
        )

        if habit.reward:
            text += f"\nНаграда: {habit.reward}"

        try:
            send_telegram_message(habit.user.tg_chat_id, text)
        except Exception as e:
            print(f"Ошибка отправки для привычки {habit.id}: {e}")
