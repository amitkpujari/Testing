from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

class Command(BaseCommand):
    help = 'Creates 100 users'

    def handle(self, *args, **kwargs):
        for i in range(100):
            username = f'user{i}'
            email = f'{username}@nsl.co.in'
            password = get_random_string(length=10)
            User.objects.create_user(username=username, email=email, password=password)
