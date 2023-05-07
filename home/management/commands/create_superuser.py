# home/management/commands/create_test_users.py
from django.core.management.base import BaseCommand
from home.models import User
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Creates test users'

    def handle(self, *args, **options):
        user = User.objects.create(
            email='unotest.campus@gmail.com',
            password=make_password('UnoMis@2023'),
            is_superuser=False,
            is_staff=False,
            is_campuspartner=True,
        )

        user2 = User.objects.create(
            email='unotest1.super@gmail.com',
            password=make_password('UnoMis@2023'),
            is_superuser=True,
            is_staff=True,
        )
