from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import CustomUser

from .models import Workplace


# Create your views here.
class CanMoveEmployeesPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm("workspace.can_move_employees")


class MoveEmployeeAPIView(APIView):
    permission_classes = [CanMoveEmployeesPermission]

    def post(self, request, *args, **kwargs):
        user_id = request.data.get("user_id")
        target_table_number = request.data.get("target_table_number")

        user = get_object_or_404(CustomUser, pk=user_id)
        target_workplace = get_object_or_404(
            Workplace, table_number=target_table_number
        )

        target_workplace.occupied_by = user
        try:
            target_workplace.full_clean()
            target_workplace.save()
            return Response(
                {
                    "status": "success",
                    "message": f"{user.username} перемещен за стол {target_table_number}",
                },
                status=status.HTTP_200_OK,
            )
        except ValidationError as e:
            return Response(
                {"status": "error", "message": e.messages},
                status=status.HTTP_400_BAD_REQUEST,
            )
