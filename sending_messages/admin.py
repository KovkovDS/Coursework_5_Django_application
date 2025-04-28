from django.contrib import admin
from .models import MailingRecipient


@admin.register(MailingRecipient)
class MailingRecipientAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'initials', 'owner',)
    list_filter = ('email', 'initials',)
    search_fields = ('email', 'initials',)
