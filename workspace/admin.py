from django.contrib import admin
from .models import Workplace


# Register your models here.
@admin.register(Workplace)
class WorkplaceAdmin(admin.ModelAdmin):
    list_display = ('table_number', 'occupied_by', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('table_number', 'occupied_by__user__first_name',
                     'occupied_by__user__last_name')
