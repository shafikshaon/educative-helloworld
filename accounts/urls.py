from django.urls import path

from accounts.views import LoginView

app_label = 'accounts'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
]
