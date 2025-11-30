from django.urls import path

from .views import MoveEmployeeAPIView

urlpatterns = [
    path("move_employee/", MoveEmployeeAPIView.as_view(), name="api-move-employee"),
]
