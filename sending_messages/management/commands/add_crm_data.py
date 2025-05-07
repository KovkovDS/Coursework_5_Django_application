from django.core.management.base import BaseCommand
from django.core.management import call_command
from sending_messages.models import Mailing, Message, MailingRecipient, MailingAttempt


class Command(BaseCommand):
    help = 'Load test data for groups from fixture'

    def handle(self, *args, **kwargs):
        Mailing.objects.all().delete()
        Message.objects.all().delete()
        MailingRecipient.objects.all().delete()
        MailingAttempt.objects.all().delete()

        call_command('loaddata', 'crm_data_fixture.json')
        self.stdout.write(self.style.SUCCESS('Successfully loaded data from fixture'))
