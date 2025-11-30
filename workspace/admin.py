from django import forms
from django.contrib import admin

from .models import Workplace


class WorkplaceAdminForm(forms.ModelForm):
    class Meta:
        model = Workplace
        fields = "__all__"

    def clean(self):
        self.instance.clean()
        return super().clean()


@admin.register(Workplace)
class WorkplaceAdmin(admin.ModelAdmin):
    form = WorkplaceAdminForm

    list_display = ("table_number", "occupied_by", "is_active")
    list_filter = ("is_active",)
    search_fields = (
        "table_number",
        "occupied_by__first_name",
        "occupied_by__last_name",
        "occupied_by__username",
    )
