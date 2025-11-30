from django.core.exceptions import ValidationError
from django.test import TestCase

from assignment.models import EmployeeSkill, Skill
from users.models import CustomUser
from workspace.models import Workplace


class WorkplaceValidatorTests(TestCase):
    def setUp(self):
        self.skill_tester = Skill.objects.create(name="Тестировщик")
        self.skill_dev = Skill.objects.create(name="Бэкенд")
        self.skill_manager = Skill.objects.create(name="Менеджер")

        self.dev_user = CustomUser.objects.create_user(
            username="dev_user", first_name="Dev", last_name="User"
        )
        EmployeeSkill.objects.create(user=self.dev_user, skill=self.skill_dev, level=8)

        self.tester_user = CustomUser.objects.create_user(
            username="tester_user", first_name="Tester", last_name="User"
        )
        EmployeeSkill.objects.create(
            user=self.tester_user, skill=self.skill_tester, level=5
        )

        self.manager_user = CustomUser.objects.create_user(
            username="manager_user", first_name="Manager", last_name="User"
        )
        EmployeeSkill.objects.create(
            user=self.manager_user, skill=self.skill_manager, level=5
        )

        self.workplace_1 = Workplace.objects.create(table_number=1, is_active=True)
        self.workplace_2 = Workplace.objects.create(table_number=2, is_active=True)
        self.workplace_3 = Workplace.objects.create(table_number=3, is_active=True)

    def test_validator_raises_error_for_neighboring_conflicting_roles(self):

        self.workplace_2.occupied_by = self.tester_user
        self.workplace_2.save()

        self.workplace_1.occupied_by = self.dev_user

        with self.assertRaises(ValidationError):
            self.workplace_1.clean()

        self.workplace_3.occupied_by = self.dev_user
        with self.assertRaises(ValidationError):
            self.workplace_3.clean()

    def test_validator_allows_neighboring_non_conflicting_roles(self):

        self.workplace_2.occupied_by = self.tester_user
        self.workplace_2.save()

        self.workplace_1.occupied_by = self.manager_user

        try:
            self.workplace_1.clean()
        except ValidationError:
            self.fail(
                "ValidationError была вызвана для совместимых ролей ("
                "менеджер/тестировщик)"
            )

    def test_validator_allows_non_neighboring_conflicting_roles(self):

        self.workplace_1.occupied_by = self.tester_user
        self.workplace_1.save()

        self.workplace_3.occupied_by = self.dev_user

        try:
            self.workplace_3.clean()
        except ValidationError:
            self.fail("ValidationError была вызвана для не соседних столов")
