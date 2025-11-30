from datetime import date, timedelta

from django.test import TestCase
from django.urls import reverse

from assignment.models import EmployeeSkill, Skill
from users.models import CustomUser


class UserDetailViewTests(TestCase):
    def setUp(self):
        self.skill_dev = Skill.objects.create(name="Бэкенд")
        today = date.today()

        self.user1 = CustomUser.objects.create_user(
            username="user1",
            first_name="Иван",
            last_name="Иванов",
            email="user1@example.com",
            hire_date=today - timedelta(days=100),
            gender="M",
        )
        EmployeeSkill.objects.create(user=self.user1, skill=self.skill_dev, level=8)

        self.url = reverse("users:user_detail", kwargs={"pk": self.user1.pk})

    def test_detail_page_requires_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_detail_page_available_to_authenticated_user(self):
        authenticated_client = self.client_class()
        authenticated_client.force_login(self.user1)

        response = authenticated_client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/user_detail.html")
        self.assertContains(response, "Подробная информация о сотруднике")

    def test_detail_page_context_data(self):
        authenticated_client = self.client_class()
        authenticated_client.force_login(self.user1)
        response = authenticated_client.get(self.url)

        self.assertIsInstance(response.context["object"], CustomUser)
        self.assertEqual(response.context["object"].username, "user1")

        self.assertContains(response, "Бэкенд")
        self.assertContains(response, "Уровень 8/10")

        self.assertContains(response, "Стаж работы:")
        self.assertGreater(response.context["object"].years_of_service(), -1)

        self.assertContains(response, "Мужской")
