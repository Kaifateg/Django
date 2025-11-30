from django.contrib import admin

from .models import EmployeeSkill, Skill


# Register your models here.
@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
