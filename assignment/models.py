from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


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
        related_name='skill_levels',
        verbose_name="Сотрудник"
    )
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, verbose_name="Навык")
    level = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="Уровень освоения (1-10)"
    )

    class Meta:
        unique_together = ('user', 'skill')
        verbose_name = "Уровень навыка сотрудника"
        verbose_name_plural = "Уровни навыков сотрудников"

    def __str__(self):
        return f"{self.user} - {self.skill.name}: Уровень {self.level}"

