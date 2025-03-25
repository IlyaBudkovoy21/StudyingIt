from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status

from listTasks.models import Tasks, CodePatterns, Types
from StudyingIt.settings import SERVICES


class CodeMonitoringTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username="testName", password="testPass")
        testCat = Types.objects.create(catTask="testCat")
        testPattern = CodePatterns.objects.create(python="testPy", cpp="testCpp", go="testFo")
        cls.task = Tasks.objects.create(name="testName", desc="testDesc", cat=testCat, patterns=testPattern)
        cls.NONEXISTENT_ID = 9

    def setUp(self):
        super().setUp()
        self.client.defaults['HTTP_X_REAL_IP'] = SERVICES[0]

    def test_permission(self):
        response = self.client.post(reverse("update_days_solutions"), data={"id": 1, "task_id": 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(reverse("update_days_solutions"), data={"id": 1, "task_id": 1},
                                    HTTP_X_REAL_IP="127.0.0.1")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_correct_input(self):
        response = self.client.post(reverse("update_days_solutions"), data={"id": self.NONEXISTENT_ID, "task_id": 1})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.post(reverse("update_days_solutions"), data={"id": 1, "task_id": self.NONEXISTENT_ID})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.post(reverse("update_days_solutions"), data={"id": self.NONEXISTENT_ID, "task_id": self.NONEXISTENT_ID})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.post(reverse("update_days_solutions"), data={"task_id": self.NONEXISTENT_ID})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(reverse("update_days_solutions"), data={"id": self.NONEXISTENT_ID})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(reverse("update_days_solutions"), data={"id": 1, "task_id": 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "Success data save")
