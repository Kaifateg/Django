from django.views.generic import DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CustomUser


# Create your views here.
class HomeView(ListView):
    model = CustomUser
    template_name = 'users/home.html'
    queryset = CustomUser.objects.exclude(username='admin').order_by('first_name')[:5]


class UserListView(ListView):
    model = CustomUser
    template_name = 'users/user_list.html'
    queryset = CustomUser.objects.exclude(username='admin').order_by(
        'first_name')


class UserDetailView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'users/user_detail.html'
