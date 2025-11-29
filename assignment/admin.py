from django.contrib import admin
from .models import Skill, EmployeeSkill


# Register your models here.
@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
