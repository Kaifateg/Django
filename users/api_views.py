from django.db import models

from rest_framework import generics, permissions, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated

from .filters import CustomUserFilter
from .models import CustomUser
from .serializer import CustomUserSerializer

# Create your views here.
base_employee_queryset = (
    CustomUser.objects.exclude(
        models.Q(first_name__exact="") | models.Q(last_name__exact="")
    )
    .exclude(username="admin")
    .order_by("first_name")
)


class StandardResultsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"


class EmployeeListAPIView(generics.ListAPIView):
    queryset = base_employee_queryset
    serializer_class = CustomUserSerializer
    pagination_class = StandardResultsPagination
    permission_classes = [permissions.AllowAny]


class FilteredEmployeeListAPIView(generics.ListAPIView):
    queryset = base_employee_queryset
    serializer_class = CustomUserSerializer
    pagination_class = StandardResultsPagination

    filterset_class = CustomUserFilter
    search_fields = ["first_name", "last_name", "username", "email"]
    permission_classes = [permissions.AllowAny]


class EmployeeDetailAPIView(generics.RetrieveAPIView):
    queryset = base_employee_queryset
    serializer_class = CustomUserSerializer
    lookup_field = "pk"
    permission_classes = [permissions.AllowAny]


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = base_employee_queryset
    serializer_class = CustomUserSerializer
    search_fields = ["first_name", "last_name", "username", "email"]

    def get_permissions(self):

        if self.action in ["list", "retrieve"]:
            permission_classes = [permissions.AllowAny]
        elif self.action in ["create", "update", "partial_update", "destroy"]:
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.DjangoModelPermissions]

        return [permission() for permission in permission_classes]
