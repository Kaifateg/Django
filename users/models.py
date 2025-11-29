from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField


# Create your models here.
class CustomUser(AbstractUser):
    GENDER_CHOICES = (
        ('M', 'Мужской'),
        ('F', 'Женский'),
    )

    patronymic = models.CharField(max_length=100, blank=True, null=True,
                                  verbose_name="Отчество")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True,
                              null=True, verbose_name="Пол")

    description = RichTextField(blank=True, null=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Пользователь/Сотрудник"
        verbose_name_plural = "Пользователи/Сотрудники"

    def __str__(self):
        full_name = f"{self.first_name} {self.last_name}"
        if self.patronymic:
            full_name += f" {self.patronymic}"
        return full_name.strip() or self.username
