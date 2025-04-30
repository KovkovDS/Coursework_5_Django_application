from django.core.mail import send_mail
from django.core.management import BaseCommand
from django.utils import timezone
from crm.settings import EMAIL_HOST_USER
from sending_messages.models import Mailing, MailingAttempt


class Command(BaseCommand):
    """Отправка сообщений"""
    def handle(self, *args, **kwargs):
        mailings = Mailing.objects.filter(status__in=[Mailing.STATUS_CHOICES["CREATED"],
                                                      Mailing.STATUS_CHOICES["LAUNCHED"]])
        for mailing in mailings:
            for recipient in mailing.recipients.all():
                try:
                    send_mail(
                        mailing.message.subject,
                        mailing.message.content,
                        from_email=EMAIL_HOST_USER,
                        recipient_list=[recipient.email],
                        fail_silently=False,
                    )
                    MailingAttempt.objects.create(
                        date_attempt=timezone.now(),
                        status=MailingAttempt.STATUS_CHOICES["SUCCESSFULLY"],
                        server_response="Сообщение отправлено.",
                        mailing=mailing,
                    )
                    print(f"Сообщение {mailing.message.subject} успешно отправлено на  {recipient.email}")
                except Exception as e:
                    MailingAttempt.objects.create(
                        date_attempt=timezone.now(),
                        status=MailingAttempt.STATUS_CHOICES["NOT SUCCESSFUL"],
                        server_response=str(e),
                        mailing=mailing,
                    )
                    print(str(e))
            mailing.save()
