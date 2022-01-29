from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from faker import Faker


class Command(BaseCommand):
    help = 'Generate superuser'

    def handle(self, *args, **kwargs):
        try:
            User.objects.create_superuser(username='educative', email='educative@mail.com',password='p@ss1234')
            self.stdout.write('Create superuser.')
        except:
            pass

        fake = Faker()
        # Create users
        total_user = User.objects.count()
        if total_user >= 20:
            pass
        else:
            for i in range(20):
                u = User()
                u.email = fake.email()
                u.first_name = fake.first_name()
                u.last_name = fake.last_name()
                u.username = fake.user_name()
                u.set_password('p@ss1234')
                u.save()
