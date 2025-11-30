from django.contrib.auth.mixins import UserPassesTestMixin


class ViewerRequiredMixin(UserPassesTestMixin):
    def test_func(self):

        return self.request.user.groups.filter(name__in=['Посетители',
                                                         'Смотрители',
                                                         'Администраторы']).exists()
