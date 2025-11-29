from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from assignment.models import EmployeeSkill
from .models import CustomUser


# Register your models here.
class EmployeeSkillInline(admin.TabularInline):
    model = EmployeeSkill
    extra = 1


class CustomUserAdmin(UserAdmin):
    inlines = [EmployeeSkillInline, ]
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'patronymic',
        'is_staff',
    )

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {
            'fields': (
                'first_name',
                'last_name',
                'patronymic',  # Отчество
                'email',
                'gender',  # Пол
                'description',  # Описание (RichTextField)
            )
        }),
        ('Разрешения и группы', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups',
                       'user_permissions'),
        }),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )

    # Также обновляем набор полей для формы создания НОВОГО пользователя
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name',
                       'patronymic', 'gender', 'description', 'password',
                       'password2'),
        }),
    )

    search_fields = ('username', 'email', 'first_name', 'last_name',
                     'patronymic')


admin.site.register(CustomUser, CustomUserAdmin)
