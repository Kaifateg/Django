from django.db import models
from django.conf import settings


# Create your models here.
class Workplace(models.Model):
    table_number = models.CharField(max_length=50, unique=True,
                                    verbose_name="Номер стола")

    occupied_by = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='workplace',
        verbose_name="Занято сотрудником"
    )

    is_active = models.BooleanField(default=True, verbose_name="Активно")

    class Meta:
        verbose_name = "Рабочее место (стол)"
        verbose_name_plural = "Рабочие места (столы)"
        ordering = ['table_number']

    def __str__(self):
        status = " (Свободно)" if not self.occupied_by else f" (Занято: {self.occupied_by})"
        return f"Стол №{self.table_number}{status}"
