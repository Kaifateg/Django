from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q


# Create your models here.
class Workplace(models.Model):
    table_number = models.PositiveIntegerField(unique=True, verbose_name="Номер стола")

    occupied_by = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="workplace",
        verbose_name="Занято сотрудником",
    )

    is_active = models.BooleanField(default=True, verbose_name="Активно")

    def clean(self):
        super().clean()

        if not self.occupied_by:
            return

        current_table_int = self.table_number

        neighbor_table_numbers = [current_table_int - 1, current_table_int + 1]

        neighbor_workplaces = Workplace.objects.filter(
            Q(table_number__in=neighbor_table_numbers) & Q(is_active=True)
        ).exclude(pk=self.pk)

        current_user_roles = self.get_user_roles(self.occupied_by)

        for neighbor_workplace in neighbor_workplaces:
            if neighbor_workplace.occupied_by:
                neighbor_user_roles = self.get_user_roles(
                    neighbor_workplace.occupied_by
                )

                if self.are_roles_incompatible(current_user_roles, neighbor_user_roles):
                    raise ValidationError(
                        f"Невозможно посадить сотрудника за стол №"
                        f"{self.table_number}. "
                        f"За соседним столом №"
                        f"{neighbor_workplace.table_number} сидит сотрудник "
                        f"несовместимой роли."
                    )

    @staticmethod
    def get_user_roles(user):
        roles = []
        skills = user.skill_levels.all().select_related("skill")
        for es in skills:
            skill_name = es.skill.name.lower()
            if "тестировщик" in skill_name:
                roles.append("tester")
            elif (
                "фронтенд" in skill_name
                or "бэкенд" in skill_name
                or "разработчик" in skill_name
            ):
                roles.append("developer")
        return roles

    @staticmethod
    def are_roles_incompatible(roles1, roles2):
        is_tester1 = "tester" in roles1
        is_dev1 = "developer" in roles1
        is_tester2 = "tester" in roles2
        is_dev2 = "developer" in roles2

        if (is_tester1 and is_dev2) or (is_dev1 and is_tester2):
            return True
        return False

    class Meta:
        verbose_name = "Рабочее место (стол)"
        verbose_name_plural = "Рабочие места (столы)"
        ordering = ["table_number"]
        permissions = [
            ("can_move_employees", "Can move employees between workplaces"),
        ]

    def __str__(self):
        status = (
            " (Свободно)" if not self.occupied_by else f" (Занято: {self.occupied_by})"
        )
        return f"Стол №{self.table_number}{status}"
