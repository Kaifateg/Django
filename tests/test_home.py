from datetime import date, timedelta

from django.test import TestCase
from django.urls import reverse

from assignment.models import EmployeeSkill, Skill
from users.models import CustomUser


class HomeViewTests(TestCase):
    def setUp(self):

        self.skill_tester = Skill.objects.create(name="Тестировщик")
        self.skill_dev = Skill.objects.create(name="Бэкенд")

        today = date.today()

        self.user1 = CustomUser.objects.create_user(
            username="user1",
            first_name="Иван",
            last_name="Иванов",
            email="user1@example.com",
            hire_date=today - timedelta(days=500),  # Принят 500 дней назад
        )
        EmployeeSkill.objects.create(user=self.user1, skill=self.skill_dev, level=8)

        self.user2 = CustomUser.objects.create_user(
            username="user2",
            first_name="Петр",
            last_name="Петров",
            email="user2@example.com",
            hire_date=today - timedelta(days=10),
        )
        EmployeeSkill.objects.create(user=self.user2, skill=self.skill_tester, level=5)

        self.user3 = CustomUser.objects.create_user(
            username="user3",
            first_name="Алексей",
            last_name="Алексеев",
            email="user3@example.com",
            hire_date=today - timedelta(days=30),
        )

        self.user_no_date = CustomUser.objects.create_user(
            username="no_date_user",
            first_name="Без",
            last_name="Даты",
            email="no_date@example.com",
            hire_date=None,
        )

        self.user5 = CustomUser.objects.create_user(
            username="user5",
            first_name="Василий",
            last_name="Васильев",
            email="user5@example.com",
            hire_date=today - timedelta(days=1),
        )

        self.user6 = CustomUser.objects.create_user(
            username="user6",
            first_name="Шестой",
            last_name="Тест",
            email="user6@example.com",
            hire_date=today - timedelta(days=2),
        )

        self.url = reverse("users:home")

    def test_home_page_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_home_page_available_to_anonymous_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Добро пожаловать в проект SeatSync")

    def test_home_page_available_to_authenticated_user(self):

        authenticated_client = self.client_class()
        authenticated_client.force_login(self.user1)

        response = authenticated_client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Добро пожаловать в проект SeatSync")

    def test_home_page_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "users/home.html")
        self.assertTemplateUsed(response, "base.html")
        self.assertTemplateUsed(response, "includes/users/user_stats.html")

    def test_home_page_context_total_count(self):

        response = self.client.get(self.url)

        self.assertEqual(response.context["total_employees_count"], 6)

    def test_home_page_context_latest_four_employees(self):

        response = self.client.get(self.url)

        self.assertEqual(len(response.context["object_list"]), 4)

        self.assertEqual(
            response.context["object_list"][0].username, self.user5.username
        )
        self.assertEqual(
            response.context["object_list"][1].username, self.user6.username
        )
        self.assertEqual(
            response.context["object_list"][2].username, self.user2.username
        )
        self.assertEqual(
            response.context["object_list"][3].username, self.user3.username
        )

    def test_home_page_only_four_users_displayed(self):

        response = self.client.get(self.url)

        self.assertEqual(len(response.context["object_list"]), 4)

        usernames_in_list = [user.username for user in response.context["object_list"]]
        self.assertNotIn(self.user1.username, usernames_in_list)
