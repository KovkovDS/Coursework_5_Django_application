from django.db import models
from users.models import User


class MailingRecipient(models.Model):

    email = models.EmailField(unique=True, verbose_name='Адрес электронной почты (Login)')
    initials = models.CharField(max_length=150, blank=True, null=True, verbose_name='Ф. И. О.')
    comment = models.TextField(default='Здесь пока ничего нет.', blank=True, null=True, verbose_name='Комментарий')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец')

    def __str__(self):
        return f'\n\nМенеджер клиента: {self.owner.email}.\nФ. И. О. клиента: {self.initials}.' \
               f'\nАдрес электронной почты (Login): {self.email}.'

    class Meta:
        verbose_name = 'Получатель рассылки'
        verbose_name_plural = 'Получатели рассылки'
        ordering = ['owner', 'email', 'initials']


class Message(models.Model):

    message_subject = models.CharField(max_length=150, verbose_name='Тема письма')
    message_body = models.TextField(default='Это тестовое письмо, не отвечайте на него.', verbose_name='Тело письма')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец')

    def __str__(self):
        return f'\n\nАвтор письма: {self.owner.email}.\nТема письма: {self.message_subject}.'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['owner', 'message_subject']
