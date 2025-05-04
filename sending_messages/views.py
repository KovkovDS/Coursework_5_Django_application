from django.urls import reverse, reverse_lazy
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from sending_messages.forms import MailingRecipientForm, MessageForm, MailingForm
from sending_messages.models import MailingRecipient, Message, Mailing, MailingAttempt
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator


@method_decorator(cache_page(60 * 15), name='dispatch')
class MailingRecipientListView(ListView):
    paginate_by = 4
    model = MailingRecipient
    template_name = 'recipients.html'
    context_object_name = 'recipients'

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_superuser or self.request.user.groups.filter(name="Менеджеры"):
            return super().get_queryset()
        elif self.request.user.groups.filter(name="Пользователи"):
            return super().get_queryset().filter(owner=self.request.user)
        raise PermissionDenied


@method_decorator(cache_page(60 * 15), name='dispatch')
class MailingRecipientDetailView(LoginRequiredMixin, DetailView):
    model = MailingRecipient
    template_name = 'recipient.html'


class MailingRecipientCreateView(LoginRequiredMixin, CreateView):
    model = MailingRecipient
    form_class = MailingRecipientForm
    template_name = 'adding_recipient.html'

    def form_valid(self, form):
        recipient = form.save()
        recipient.owner = self.request.user
        recipient.save()

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

    def get_success_url(self, **kwargs):
        return reverse('sending_messages:recipient', args=[self.kwargs.get('pk')])


class MailingRecipientDeleteView(LoginRequiredMixin, DeleteView):
    model = MailingRecipient
    template_name = 'recipients_confirm_delete.html'
    success_url = reverse_lazy('sending_messages:recipients')


@method_decorator(cache_page(60 * 15), name='dispatch')
class MessageListView(ListView):
    paginate_by = 4
    model = Message
    template_name = 'messages.html'
    context_object_name = 'messages'

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_superuser or self.request.user.groups.filter(name="Менеджеры"):
            return super().get_queryset()
        elif self.request.user.groups.filter(name="Пользователи"):
            return super().get_queryset().filter(owner=self.request.user)
        raise PermissionDenied


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = 'message.html'


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'adding_message.html'

    def form_valid(self, form):
        message = form.save()
        message.owner = self.request.user
        message.save()
        return super().form_valid(form)

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

    def get_success_url(self, **kwargs):
        return reverse('sending_messages:message', args=[self.kwargs.get('pk')])


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = 'messages_confirm_delete.html'
    success_url = reverse_lazy('sending_messages:messages')


@method_decorator(cache_page(60 * 15), name='dispatch')
class MailingListView(ListView):
    paginate_by = 4
    model = Mailing
    template_name = 'mailings.html'
    context_object_name = 'mailings'

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_superuser or self.request.user.groups.filter(name="Менеджеры"):
            return super().get_queryset()
        elif self.request.user.groups.filter(name="Пользователи"):
            return super().get_queryset().filter(owner=self.request.user)
        raise PermissionDenied


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = 'mailing.html'


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'adding_mailing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipients = MailingRecipient.objects.filter(owner=self.request.user)
        context['recipients'] = recipients
        return context

    def form_valid(self, form):
        mailing = form.save()
        mailing.owner = self.request.user
        mailing.save()
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse('sending_messages:added_mailing', args=[self.object.id], kwargs=self.kwargs)


class AddedMailing(LoginRequiredMixin, TemplateView):
    model = Mailing
    template_name = 'added_mailing.html'
    context_object_name = 'added_mailing'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        added_mailing = Mailing.objects.get(pk=kwargs['pk'])
        context['object'] = added_mailing
        return context


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'editing_mailing.html'

    def get_success_url(self, **kwargs):
        return reverse('sending_messages:mailing', args=[self.kwargs.get('pk')])


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = 'mailings_confirm_delete.html'
    success_url = reverse_lazy('sending_messages:mailings')


class MailingAttemptsListView(LoginRequiredMixin, ListView):
    model = MailingAttempt
    template_name = 'mailing_list_statistics.html'
    context_object_name = 'mailing_attempts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        mailings = Mailing.objects.filter(owner=user)
        mailing_attempts = MailingAttempt.objects.filter(mailing__in=mailings)

        successfully = 0
        failed = 0
        mailings_successful = 0

        for attempt in mailing_attempts:
            if attempt.status == "SUCCESSFULLY":
                successfully += 1
                mailings_successful += attempt.mailing.recipients.count()
            if attempt.status == "NOT SUCCESSFUL":
                failed += 1

        context["successful"] = successfully
        context["failed"] = failed
        context["mailings_successful"] = mailings_successful
        context["mailing_attempts_count"] = mailing_attempts.count()
        return context

    def get_queryset(self, *args, **kwargs):

        if self.request.user.groups.filter(name="Пользователи").exists():
            user = self.request.user
            mailings = Mailing.objects.filter(owner=user)
            return super().get_queryset().filter(mailing__in=mailings)
        elif self.request.user:
            return super().get_queryset()
        raise PermissionDenied


class MailingAttemptsCreateView(LoginRequiredMixin, CreateView):
    model = MailingAttempt
    template_name = 'adding_mailing_attempt.html'
    success_url = reverse_lazy('sending_messages:adding_mailing_attempt')


class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["count_mailing"] = len(Mailing.objects.all())
        active_mailings_count = Mailing.objects.filter(status="Запущена").count()
        context_data["active_mailings_count"] = active_mailings_count
        unique_recipients_count = MailingRecipient.objects.distinct().count()
        context_data["unique_recipients_count"] = unique_recipients_count
        return context_data
