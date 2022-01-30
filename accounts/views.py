from django.contrib import messages
from django.contrib.auth.views import LoginView as BaseLogin, LogoutView as BaseLogoutView
from django.utils.translation import ugettext_lazy as _

from accounts.forms.login import LoginForm


class LoginView(BaseLogin):
    template_name = "accounts/auth/login.html"
    form_class = LoginForm


class LogoutView(BaseLogoutView):

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.add_message(request, messages.SUCCESS, _('You are logged out successfully.'))
        return response
