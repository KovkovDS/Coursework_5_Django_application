from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from crm.settings import EMAIL_HOST_USER
from sending_messages.models import Mailing, MailingAttempt


def run_mailing(request, pk):
    """Функция запуска рассылки по требованию"""
    mailing = get_object_or_404(Mailing, id=pk)
    for recipient in mailing.recipients.all():
        try:
            mailing.status = Mailing.STATUS_CHOICES["LAUNCHED"]
            send_mail(
                subject=mailing.message.message_subject,
                message=mailing.message.message_body,
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
        except Exception as e:
            print(f"Ошибка при отправке письма для {recipient.email}: {str(e)}")
            MailingAttempt.objects.create(
                date_attempt=timezone.now(),
                status=MailingAttempt.STATUS_CHOICES["NOT SUCCESSFUL"],
                server_response=str(e),
                mailing=mailing,
            )
    if mailing.end_sending and mailing.end_sending <= timezone.now():
        mailing.status = Mailing.STATUS_CHOICES["COMPLETED"]
    mailing.save()
    return redirect("sending_messages:mailing-list")
