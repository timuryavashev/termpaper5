from rest_framework.serializers import ValidationError



class HabitDurationValidator:
    """ Проверяет продолжительность выполнения привычки """

    MAX_TIME_SECONDS = 120

    def __init__(self, field):

        self.field = field

    def __call__(self, data):
        tmp_val = data.get(self.field)
        if tmp_val and tmp_val.total_seconds() > self.MAX_TIME_SECONDS:
            raise ValidationError({
                "time_to_action": f"Время выполнения не может превышать {self.MAX_TIME_SECONDS} секунд."
            })


class HabitPeriodValidator:
    """ Проверяет период выполнения привычки """

    MAX_PERIOD_DAYS = 7
    MIN_PERIOD_DAYS = 1

    def __init__(self, field):

        self.field = field

    def __call__(self, data):

        tmp_val = data.get(self.field)

        if tmp_val and tmp_val > self.MAX_PERIOD_DAYS:
            raise ValidationError({
                "period": f"Нельзя выполнять привычку чаще, чем 7 раз в неделю."
            })
        if tmp_val and tmp_val < self.MAX_PERIOD_DAYS:
            raise ValidationError({
                "period": f"Нельзя выполнять привычку реже, чем 1 раз в неделю."
            })


class MutualExclusionsValidator:
    """ Проверяет, что заполнено только одно из переданных полей """

    def __init__(self, fields):

        self.fields = fields

    def __call__(self, data):

        n = 0

        for x in self.fields:
            if data.get(x):
                n += 1

        if n > 1:
            raise ValidationError(f'Должно быть заполнено только одно из полей: {', '.join(self.fields)}.')
