from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .api_views import EmployeeListAPIView, \
    FilteredEmployeeListAPIView, EmployeeDetailAPIView, EmployeeViewSet


router = DefaultRouter()
router.register(r'view/employees', EmployeeViewSet, basename='employee')

urlpatterns = [
    path('employees/', EmployeeListAPIView.as_view(),
         name='employee-list-api'),
    path('employees/filter/', FilteredEmployeeListAPIView.as_view(),
         name='employee-filter-api'),
    path('employees/<int:pk>/', EmployeeDetailAPIView.as_view(),
         name='employee-detail-api'),
    path('', include(router.urls)),
]
