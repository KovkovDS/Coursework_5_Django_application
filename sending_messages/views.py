from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from sending_messages.forms import MailingRecipientForm, MessageForm
from sending_messages.models import MailingRecipient, Message


class MailingRecipientListView(ListView):
    paginate_by = 4
    model = MailingRecipient
    template_name = 'recipients.html'
    context_object_name = 'recipients'


class MailingRecipientDetailView(LoginRequiredMixin, DetailView):
    model = MailingRecipient
    template_name = 'recipient.html'
    context_object_name = 'recipient'


class MailingRecipientCreateView(LoginRequiredMixin, CreateView):
    model = MailingRecipient
    form_class = MailingRecipientForm
    template_name = 'adding_recipient.html'

    def get_success_url(self, **kwargs):
        return reverse('sending_messages:added_recipient', args=[self.object.id], kwargs=self.kwargs)


class AddedMailingRecipient(LoginRequiredMixin, TemplateView):
    model = MailingRecipient
    template_name = 'added_recipient.html'
    context_object_name = 'added_recipient'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        added_recipient = MailingRecipient.objects.get(pk=kwargs['pk'])
        context['object'] = added_recipient
        return context


class MailingRecipientUpdateView(LoginRequiredMixin, UpdateView):
    model = MailingRecipient
    form_class = MailingRecipientForm
    template_name = 'editing_recipient.html'


class MailingRecipientDeleteView(LoginRequiredMixin, DeleteView):
    model = MailingRecipient
    template_name = 'recipients_confirm_delete.html'


class MessageListView(ListView):
    paginate_by = 4
    model = Message
    template_name = 'messages.html'
    context_object_name = 'messages'


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = 'message.html'
    context_object_name = 'message'


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'adding_message.html'

    def get_success_url(self, **kwargs):
        return reverse('sending_messages:added_message', args=[self.object.id], kwargs=self.kwargs)


class AddedMessage(LoginRequiredMixin, TemplateView):
    model = Message
    template_name = 'added_message.html'
    context_object_name = 'added_message'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        added_message = Message.objects.get(pk=kwargs['pk'])
        context['object'] = added_message
        return context


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'editing_message.html'


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = 'messages_confirm_delete.html'
