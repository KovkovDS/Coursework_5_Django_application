from django.urls import path
from sending_messages.apps import SendingMessagesConfig
from .services import run_mailing, block_mailing
from .views import (MailingRecipientListView, MailingRecipientDetailView, MailingRecipientCreateView,
                    AddedMailingRecipient, MailingRecipientUpdateView, MailingRecipientDeleteView,
                    MessageListView, MessageDetailView, MessageCreateView, AddedMessage, MessageUpdateView,
                    MessageDeleteView,
                    MailingListView, MailingDetailView, MailingCreateView, AddedMailing,
                    MailingUpdateView, MailingDeleteView, MailingListStatisticsView, HomePageView,
                    MailingAttemptsListView, MailingAttemptsCreateView
                    )


app_name = SendingMessagesConfig.name

urlpatterns = [
    path('recipients/', MailingRecipientListView.as_view(), name='recipients'),
    path('recipient/<int:pk>/', MailingRecipientDetailView.as_view(), name='recipient'),
    path('recipient/new/', MailingRecipientCreateView.as_view(), name='adding_recipient'),
    path('recipient/<int:pk>/added/', AddedMailingRecipient.as_view(), name='added_recipient'),
    path('recipient/<int:pk>/edit/', MailingRecipientUpdateView.as_view(), name='editing_recipient'),
    path('recipient/<int:pk>/delete/', MailingRecipientDeleteView.as_view(), name='deleting_recipient'),
    path('messages/', MessageListView.as_view(), name='messages'),
    path('message/<int:pk>/', MessageDetailView.as_view(), name='message'),
    path('message/new/', MessageCreateView.as_view(), name='adding_message'),
    path('message/<int:pk>/added/', AddedMessage.as_view(), name='added_message'),
    path('message/<int:pk>/edit/', MessageUpdateView.as_view(), name='editing_message'),
    path('message/<int:pk>/delete/', MessageDeleteView.as_view(), name='deleting_message'),
    path('mailings/', MailingListView.as_view(), name='mailings'),
    path('mailing/<int:pk>/', MailingDetailView.as_view(), name='mailing'),
    path('mailing/new/', MailingCreateView.as_view(), name='adding_mailing'),
    path('mailing/<int:pk>/added/', AddedMailing.as_view(), name='added_mailing'),
    path('mailing/<int:pk>/edit/', MailingUpdateView.as_view(), name='editing_mailing'),
    path('mailing/<int:pk>/delete/', MailingDeleteView.as_view(), name='deleting_mailing'),
    path('mailing-attempts/', MailingAttemptsListView.as_view(), name='mailing-attempts'),
    path('mailing/<int:pk>/edit/', MailingAttemptsCreateView.as_view(), name='adding_mailing_attempt'),
    path('mailing/<int:pk>/run/', run_mailing, name='run_mailing'),
    path('mailing/<int:pk>/block/', block_mailing, name='block_mailing'),
    path('statistic/', MailingListStatisticsView.as_view(), name='statistic'),
    path('', HomePageView.as_view(), name='home'),
]
