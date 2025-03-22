from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status

from listTasks.models import Tasks


class CodeMonitoringTest(APITestCase):
    def setUp(self):
        self.user = User.objects.get(id=3)
        self.task = Tasks.objects.get(id=10)

    def test_input_data(self):
        response = self.client.post(reverse("update_days_solutions"), data={"test_id": "error", "id": "error"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "Not enough information to save")

