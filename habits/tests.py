from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.serializers import ValidationError

from users.models import CustomUser


class HabitTestCase(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(username="username", password="password")

    def test_create_habit(self):
        """ Тестирование создания привычки """

        self.client.force_authenticate(user=self.user)

        data = {
            "place": "Test place",
            "time": "00:00",
            "action": "Test action"
        }

        response = self.client.post('/habit/create/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        habit_id = response.json()["id"]
        self.assertEqual(
            response.json(),
            {
                'id': habit_id,
                'place': 'Test place',
                'time': '00:00:00',
                'action': 'Test action',
                'is_pleasant': False,
                'period': 7,
                'reward': None,
                'time_to_action': '00:01:00',
                'is_published': False,
                'user': self.user.id,
                'connection_wont': None
            },
        )

    def test_update_habit(self):
        """ Тестирование обновления привычки """

        self.client.force_authenticate(user=self.user)

        data = {
            "place": "Test place",
            "time": "00:00",
            "action": "Test action"
        }
        create_response = self.client.post('/habit/create/', data=data)
        habit_id = create_response.json()["id"]
        update_data = {"place": "Test update place"}
        update_response = self.client.patch(f'/habit/update/{habit_id}/', data=update_data)
        self.assertEqual(
            update_response.json(),
            {
                'id': habit_id,
                'place': 'Test update place',
                'time': '00:00:00',
                'action': 'Test action',
                'is_pleasant': False,
                'period': 7,
                'reward': None,
                'time_to_action': '00:01:00',
                'is_published': False,
                'user': self.user.id,
                'connection_wont': None
            },
        )

    def test_delete_habit(self):
        """ Тестирование удаления привычки """

        self.client.force_authenticate(user=self.user)
        data = {
            "place": "Test place",
            "time": "00:00",
            "action": "Test action"
        }
        create_response = self.client.post('/habit/create/', data=data)
        habit_id = create_response.json()["id"]
        get_response = self.client.get('/habits/')
        self.assertEqual(
            get_response.json().get("results"),
            [
                {
                    'id': habit_id,
                    'place': 'Test place',
                    'time': '00:00:00',
                    'action': 'Test action',
                    'is_pleasant': False,
                    'period': 7,
                    'reward': None,
                    'time_to_action': '00:01:00',
                    'is_published': False,
                    'user': self.user.id,
                    'connection_wont': None
                }
            ]
        )
        self.client.delete(f'/habit/delete/{habit_id}/')
        get_response_after_delete = self.client.get('/habits/')
        self.assertEqual(get_response_after_delete.json().get("results"), [])


class ValidatorTestCase(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(username="username", password="password")

    def test_period_validator(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "place": "Test place",
            "time": "00:00",
            "action": "Test action",
            "period": 8
        }
        response = self.client.post('/habit/create/', data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {"period": ["Нельзя выполнять привычку чаще, чем 7 раз в неделю."]}
        )

    def test_duration_validator(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "place": "Test place",
            "time": "00:00",
            "action": "Test action",
            "time_to_action": 200
        }
        response = self.client.post('/habit/create/', data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {'time_to_action': ['Время выполнения не может превышать 120 секунд.']}
        )

    def test_mutual_exclusions_validator(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "place": "Test place",
            "time": "00:00",
            "action": "Test action"
        }
        response = self.client.post('/habit/create/', data=data)
        habit_id = response.json()["id"]
        data = {
            "place": "Test place",
            "time": "00:00",
            "action": "Test action",
            "reward": "Test reward",
            "connection_wont": habit_id
        }

        response = self.client.post('/habit/create/', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {'non_field_errors': ['Должно быть заполнено только одно из полей: reward, connection_wont.']}
        )