from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from sending_messages.forms import MailingRecipientForm
from sending_messages.models import MailingRecipient


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
