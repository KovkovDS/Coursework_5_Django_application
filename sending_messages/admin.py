from django.contrib import admin
from .models import MailingRecipient, Message, Mailing


@admin.register(MailingRecipient)
class MailingRecipientAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'initials', 'owner',)
    list_filter = ('email', 'initials',)
    search_fields = ('email', 'initials',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'message_subject', 'owner')
    list_filter = ('message_subject',)
    search_fields = ('message_subject',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'first_sending', 'end_sending', 'message', 'owner')
    list_filter = ('status', 'first_sending', 'end_sending', 'message',)
    search_fields = ('status', 'first_sending', 'end_sending', 'message',)
