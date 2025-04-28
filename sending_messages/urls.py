from django.urls import path
from sending_messages.apps import SendingMessagesConfig
from .views import (MailingRecipientListView, MailingRecipientDetailView, MailingRecipientCreateView,
                    AddedMailingRecipient, MailingRecipientUpdateView, MailingRecipientDeleteView,)


app_name = SendingMessagesConfig.name

urlpatterns = [
    path('recipients/', MailingRecipientListView.as_view(), name='recipients'),
    path('recipient/<int:pk>/', MailingRecipientDetailView.as_view(), name='recipient'),
    path('recipient/new/', MailingRecipientCreateView.as_view(), name='adding_recipient'),
    path('recipient/<int:pk>/added/', AddedMailingRecipient.as_view(), name='added_recipient'),
    path('recipient/<int:pk>/edit/', MailingRecipientUpdateView.as_view(), name='editing_recipient'),
    path('recipient/<int:pk>/delete/', MailingRecipientDeleteView.as_view(), name='deleting_recipient'),
    ]
