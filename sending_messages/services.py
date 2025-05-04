import requests as requests
from django.core.cache import cache
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from crm.settings import CACHE_ENABLED
from crm.settings import EMAIL_HOST_USER
from sending_messages.models import Mailing, MailingAttempt


def run_mailing(request, pk):
    """Функция запуска рассылки по требованию"""
    mailing = get_object_or_404(Mailing, id=pk)
    for recipient in mailing.recipients.all():

        try:
            recipients_mail_servers = recipient.email.split("@", 1)[1]
            url_recipients_mail_servers = "https://" + recipients_mail_servers
            response = requests.get(url_recipients_mail_servers)
            response.raise_for_status()
            mailing.status = Mailing.STATUS_CHOICES["LAUNCHED"]
            send_mail(
                subject=mailing.message.message_subject,
                message=mailing.message.message_body,
                from_email=EMAIL_HOST_USER,
                recipient_list=[recipient.email],
                fail_silently=False,
            )
            MailingAttempt.objects.create(
                create_at=timezone.now(),
                status=MailingAttempt.STATUS_CHOICES["SUCCESSFULLY"],
                server_response="Сообщение отправлено.",
                mailing=mailing,
            )
        except Exception as e:
            print(f"Ошибка при отправке письма для {recipient.email}: {str(e)}")
            MailingAttempt.objects.create(
                create_at=timezone.now(),
                status=MailingAttempt.STATUS_CHOICES["NOT SUCCESSFUL"],
                server_response=str(e),
                mailing=mailing,
            )
    if mailing.end_sending and mailing.end_sending <= timezone.now():
        mailing.status = Mailing.STATUS_CHOICES["COMPLETED"]
    mailing.save()
    return redirect("sending_messages:mailings")


@login_required
def block_mailing(request, pk):
    mailing = Mailing.objects.get(pk=pk)
    mailing.is_active = {mailing.is_active: False, not mailing.is_active: True}[True]
    mailing.save()
    return redirect("sending_messages:mailings")


def get_mailing_from_cache():
    """Получение данных по рассылкам из кэша, если кэш пуст берем из БД."""
    if not CACHE_ENABLED:
        return Mailing.objects.all()
    key = "mailing_list"
    cache_data = cache.get(key)
    if cache_data is not None:
        return cache_data
    cache_data = Mailing.objects.all()
    cache.set(key, cache_data)
    return cache_data


def get_attempt_from_cache():
    """Получение данных по попыткам из кэша, если кэш пуст берем из БД."""
    if not CACHE_ENABLED:
        return MailingAttempt.objects.all()
    key = "attempt_list"
    cache_data = cache.get(key)
    if cache_data is not None:
        return cache_data
    cache_data = MailingAttempt.objects.all()
    cache.set(key, cache_data)
    return cache_data
