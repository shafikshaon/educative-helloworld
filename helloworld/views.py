from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


# @login_required()
def index(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    return render(request, template_name='home.html', context={})
