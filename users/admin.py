from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from assignment.models import EmployeeSkill, UserImage

from .models import CustomUser


# Register your models here.
class EmployeeSkillInline(admin.TabularInline):
    model = EmployeeSkill
    extra = 1


class UserImageInline(admin.TabularInline):
    model = UserImage
    extra = 1
    fields = (
        "image",
        "order",
    )
    ordering = ("order",)


class CustomUserAdmin(UserAdmin):

    inlines = [
        EmployeeSkillInline,
        UserImageInline,
    ]

    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "patronymic",
        "is_staff",
    )

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Персональная информация",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "patronymic",
                    "email",
                    "gender",
                    "description",
                    "hire_date",
                )
            },
        ),
        (
            "Разрешения и группы",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Важные даты", {"fields": ("last_login", "date_joined")}),
    )

    search_fields = ("username", "email", "first_name", "last_name", "patronymic")


class CustomUserCreationFormAdmin(UserAdmin):

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "first_name",
                    "last_name",
                    "patronymic",
                    "gender",
                    "description",
                    "hire_date",
                    "password",
                    "password2",
                ),
            },
        ),
    )

    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
    )
    fieldsets = ()


admin.site.register(CustomUser, CustomUserAdmin)
