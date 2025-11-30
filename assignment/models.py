from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


# Create your models here.
class Skill(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Навык")

    class Meta:
        verbose_name = "Навык"
        verbose_name_plural = "Навыки"

    def __str__(self):
        return self.name


class EmployeeSkill(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="skill_levels",
        verbose_name="Сотрудник",
    )
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, verbose_name="Навык")
    level = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="Уровень освоения (1-10)",
    )

    class Meta:
        unique_together = ("user", "skill")
        verbose_name = "Уровень навыка сотрудника"
        verbose_name_plural = "Уровни навыков сотрудников"

    def __str__(self):
        return f"{self.user} - {self.skill.name}: Уровень {self.level}"


class UserImage(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="images",
        on_delete=models.CASCADE,
        verbose_name="Сотрудник",
    )
    image = models.ImageField(upload_to="user_gallery/", verbose_name="Изображение")
    order = models.PositiveIntegerField(
        default=0, blank=True, null=True, verbose_name="Порядковый номер"
    )

    class Meta:
        verbose_name = "Изображение сотрудника"
        verbose_name_plural = "Изображения сотрудников"
        ordering = ["order", "id"]

    def __str__(self):
        return f"Изображение {self.order} для {self.user.username}"
