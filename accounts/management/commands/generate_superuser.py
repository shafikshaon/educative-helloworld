from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Generate superuser'

    def handle(self, *args, **kwargs):
        try:
            User.objects.create_superuser(username='educative', password='p@ss1234')
            self.stdout.write('Create superuser.')
        except:
            pass
