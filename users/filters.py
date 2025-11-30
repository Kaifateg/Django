import django_filters

from .models import CustomUser


class CustomUserFilter(django_filters.FilterSet):

    hire_date_min = django_filters.DateFilter(
        field_name="hire_date", lookup_expr="gte", label="Дата приема ОТ"
    )
    hire_date_max = django_filters.DateFilter(
        field_name="hire_date", lookup_expr="lte", label="Дата приема ДО"
    )

    skill = django_filters.CharFilter(
        field_name="skill_levels__skill__name", lookup_expr="icontains", label="Навык"
    )

    class Meta:
        model = CustomUser
        fields = ["hire_date", "skill_levels__skill__name"]
