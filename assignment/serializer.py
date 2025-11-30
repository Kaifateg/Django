from rest_framework import serializers
from assignment.models import EmployeeSkill, UserImage


class EmployeeSkillSerializer(serializers.ModelSerializer):
    skill_name = serializers.CharField(source='skill.name', read_only=True)

    class Meta:
        model = EmployeeSkill
        fields = ['skill_name', 'level']


class UserImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserImage
        fields = ['image', 'order']
