from rest_framework import serializers

from assignment.serializer import EmployeeSkillSerializer, UserImageSerializer

from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    skills = EmployeeSkillSerializer(source="skill_levels", many=True, read_only=True)
    images = UserImageSerializer(many=True, read_only=True)

    years_of_service_days = serializers.ReadOnlyField(source="years_of_service")

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "patronymic",
            "email",
            "gender",
            "hire_date",
            "years_of_service_days",
            "skills",
            "images",
        ]
