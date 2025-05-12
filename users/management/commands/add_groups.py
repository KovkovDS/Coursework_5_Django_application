from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = 'Load test data for groups from fixture'

    def handle(self, *args, **kwargs):
        Group.objects.all().delete()

        call_command('loaddata', 'groups_fixture.json')
        self.stdout.write(self.style.SUCCESS('Successfully loaded data from fixture'))
