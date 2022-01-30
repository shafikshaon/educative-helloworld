from django.contrib.auth.views import LoginView as BaseLogin

from accounts.forms.login import LoginForm


class LoginView(BaseLogin):
    template_name = "accounts/auth/login.html"
    form_class = LoginForm
