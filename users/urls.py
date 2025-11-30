from django.urls import path
from .views import HomeView, UserDetailView, UserListView


app_name = 'users'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('list/', UserListView.as_view(), name='index'),
    path('user/<pk>', UserDetailView.as_view(), name='user_detail'),
]
