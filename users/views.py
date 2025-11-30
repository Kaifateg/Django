from django.db import models
from django.views.generic import DetailView, ListView

from .mixins import ViewerRequiredMixin
from .models import CustomUser

# Create your views here.
base_employee_queryset = (
    CustomUser.objects.exclude(
        models.Q(first_name__exact="") | models.Q(last_name__exact="")
    )
    .exclude(username="admin")
    .order_by("first_name")
)


class HomeView(ListView):
    model = CustomUser
    template_name = "users/home.html"
    queryset = base_employee_queryset.filter(hire_date__isnull=False).order_by(
        "-hire_date"
    )[:4]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_employees_count"] = base_employee_queryset.count()
        return context


class UserListView(ListView):
    model = CustomUser
    template_name = "users/user_list.html"
    queryset = base_employee_queryset
    paginate_by = 10


class UserDetailView(ViewerRequiredMixin, DetailView):
    model = CustomUser
    template_name = "users/user_detail.html"
