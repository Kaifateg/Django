from datetime import date, timedelta

from django.test import TestCase
from django.urls import reverse

from assignment.models import EmployeeSkill, Skill
from users.models import CustomUser


class UserListViewTests(TestCase):
    def setUp(self):
        self.skill_tester = Skill.objects.create(name="Тестировщик")
        self.skill_dev = Skill.objects.create(name="Бэкенд")
        today = date.today()

        self.user1 = CustomUser.objects.create_user(
            username="user1",
            first_name="Иван",
            last_name="Иванов",
            email="user1@example.com",
            hire_date=today - timedelta(days=500),
        )
        EmployeeSkill.objects.create(user=self.user1, skill=self.skill_dev, level=8)
        self.user2 = CustomUser.objects.create_user(
            username="user2",
            first_name="Петр",
            last_name="Петров",
            email="user2@example.com",
            hire_date=today - timedelta(days=10),
        )
        self.user3 = CustomUser.objects.create_user(
            username="user3",
            first_name="Алексей",
            last_name="Алексеев",
            email="user3@example.com",
            hire_date=today - timedelta(days=30),
        )
        self.user_no_date = CustomUser.objects.create_user(
            username="no_date_user",
            first_name="",
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

        self.url = reverse("users:index")

    def test_user_list_page_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_user_list_available_to_anonymous_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Список всех сотрудников")

    def test_user_list_available_to_authenticated_user(self):
        authenticated_client = self.client_class()
        authenticated_client.force_login(self.user1)

        response = authenticated_client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Список всех сотрудников")

    def test_user_list_page_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "users/user_list.html")
        self.assertTemplateUsed(response, "base.html")
        self.assertTemplateUsed(response, "includes/users/user_stats.html")

    def test_user_list_context_queryset_filtering(self):
        response = self.client.get(self.url)
        usernames_in_list = [user.username for user in response.context["object_list"]]

        self.assertNotIn(self.user_no_date.username, usernames_in_list)

        self.assertIn(self.user1.username, usernames_in_list)
        self.assertIn(self.user5.username, usernames_in_list)

    def test_user_list_pagination(self):
        response = self.client.get(self.url)
        self.assertEqual(len(response.context["object_list"]), 5)
        self.assertFalse(response.context["is_paginated"])
        self.assertEqual(response.context["paginator"].num_pages, 1)


class UserListPagePaginationTests(TestCase):
    def setUp(self):
        self.url = reverse("users:index")
        today = date.today()
        self.users = []

        for i in range(1, 14):
            user = CustomUser.objects.create_user(
                username=f"user{i}",
                first_name=f"Имя{i}",
                last_name=f"Фамилия{i}",
                email=f"user{i}@example.com",
                hire_date=today - timedelta(days=i),
            )
            self.users.append(user)

    def test_pagination_for_thirteen_users(self):

        response_page_1 = self.client.get(self.url)
        self.assertEqual(response_page_1.status_code, 200)

        self.assertEqual(len(response_page_1.context["object_list"]), 10)
        self.assertEqual(response_page_1.context["page_obj"].number, 1)
        self.assertEqual(response_page_1.context["paginator"].num_pages, 2)

        response_page_2 = self.client.get(f"{self.url}?page=2")
        self.assertEqual(response_page_2.status_code, 200)

        self.assertEqual(len(response_page_2.context["object_list"]), 3)
        self.assertEqual(response_page_2.context["page_obj"].number, 2)

    def test_pagination_invalid_page_returns_last_page(self):

        response = self.client.get(f"{self.url}?page=999")
        self.assertEqual(response.status_code, 404)
