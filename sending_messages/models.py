from django.db import models

from users.models import User


class MailingRecipient(models.Model):
    """Получатель рассылки."""
    email = models.EmailField(unique=True, verbose_name='Адрес электронной почты (Login)')
    initials = models.CharField(max_length=150, blank=True, null=True, verbose_name='Ф. И. О.')
    comment = models.TextField(default='Здесь пока ничего нет.', blank=True, null=True, verbose_name='Комментарий')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Владелец')
    is_active = models.BooleanField(default=True, verbose_name="Действующий")

    def __str__(self):
        """Метод для описания человеко читаемого вида модели "Получатель рассылки"."""
        return f'\n\nМенеджер клиента: {self.owner}.\nФ. И. О. клиента: {self.initials}.' \
               f'\nАдрес электронной почты (Login): {self.email}.'

    class Meta:
        """Класс для изменения поведения полей модели "Получатель рассылки"."""
        verbose_name = 'Получатель рассылки'
        verbose_name_plural = 'Получатели рассылки'
        ordering = ['owner', 'email', 'initials']
        permissions = [
            ("can_block_recipient", "Заблокировать/разблокировать получателя рассылки"),
        ]


class Message(models.Model):
    """Сообщение."""
    message_subject = models.CharField(max_length=150, verbose_name='Тема письма')
    message_body = models.TextField(default='Это тестовое письмо, не отвечайте на него.', verbose_name='Тело письма')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Владелец')

    def __str__(self):
        """Метод для описания человеко читаемого вида модели "Сообщение"."""
        return f'\n\nАвтор письма: {self.owner}.\nТема письма: {self.message_subject}.'

    class Meta:
        """Класс для изменения поведения полей модели "Сообщение"."""
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['owner', 'message_subject']
        permissions = [
            ("can_block_message", "Заблокировать/разблокировать сообщение"),
        ]


class Mailing(models.Model):
    """Рассылка."""
    STATUS_CHOICES = {"COMPLETED": "Завершена", "CREATED": "Создана", "LAUNCHED": "Запущена"}
    first_sending = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время первой отправки')
    end_sending = models.DateTimeField(auto_now=True, verbose_name='Дата и время окончания отправки')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Создана", verbose_name='Статус')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Сообщение')
    recipients = models.ManyToManyField(MailingRecipient, verbose_name='Получатели рассылки')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Владелец')
    is_active = models.BooleanField(default=True, verbose_name="Активна")

    def __str__(self):
        """Метод для описания человеко читаемого вида модели "Рассылка"."""
        return f'\n\nАвтор рассылки: {self.owner}.\nОтправка начата: {self.first_sending}.' \
               f'\nОтправка закончена: {self.end_sending}.\nСтатус рассылки: {self.status}.' \
               f'\nСообщение для рассылки: {self.message}.\nСписок получателей: {self.recipients}.'

    class Meta:
        """Класс для изменения поведения полей модели "Рассылка"."""
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ['owner', 'first_sending', 'end_sending', 'status', 'message']
        permissions = [
            ("can_block_mailing", "Заблокировать/разблокировать рассылку"),
        ]


class MailingAttempt(models.Model):
    """Попытка рассылки."""
    STATUS_CHOICES = {"SUCCESSFULLY": "Успешно", "NOT SUCCESSFUL": "Не успешно"}
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время попытки')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, verbose_name='Статус')
    server_response = models.TextField(null=True, blank=True, verbose_name='Ответ почтового сервера')
    mailing = models.ForeignKey(Mailing, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Рассылка')

    def __str__(self):
        """Метод для описания человеко читаемого вида модели "Попытка рассылки"."""
        return f'\n\nАвтор рассылки: {self.mailing}.\nПопытка начата: {self.create_at}.' \
               f'\nСтатус попытки: {self.status}.\nОтвет почтового сервера: {self.server_response}.'

    class Meta:
        """Класс для изменения поведения полей модели "Попытка рассылки"."""
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылки'
        ordering = ['mailing', 'create_at', 'status', 'server_response']
