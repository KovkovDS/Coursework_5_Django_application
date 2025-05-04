from django import forms
from .models import MailingRecipient, Message, Mailing
from django.core.exceptions import ValidationError


class MailingRecipientForm(forms.ModelForm):
    class Meta:
        model = MailingRecipient
        fields = ['initials', 'email', 'comment']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        cleaned_recipient_pk = self.instance.pk

        if MailingRecipient.objects.filter(email=email).exclude(id=cleaned_recipient_pk).exists():
            raise ValidationError('Получатель с таким E-mail уже существует.')
        return email

    def __init__(self, *args, **kwargs):
        super(MailingRecipientForm, self).__init__(*args, **kwargs)
        self.fields['initials'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите Ф.И.О. клиента'})
        self.fields['email'].widget.attrs.update({'class': 'form-control',
                                                  'placeholder': 'Введите рабочий адрес электронной почты клиента'})
        self.fields['comment'].widget.attrs.update({'class': 'form-control', 'id': "exampleFormControlTextarea1",
                                                    'rows': "4", 'placeholder':
                                                        'Введите комментарий (описание) по данному клиенту'})


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message_subject', 'message_body']

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields['message_subject'].widget.attrs.update({'class': 'form-control',
                                                            'placeholder': 'Введите тему сообщения '})
        self.fields['message_body'].widget.attrs.update({'class': 'form-control', 'id': "exampleFormControlTextarea1",
                                                         'rows': "4", 'placeholder': 'Введите текст сообщения'})


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['message', 'recipients']

    def __init__(self, *args, **kwargs):
        super(MailingForm, self).__init__(*args, **kwargs)
        self.fields['message'].widget.attrs.update({'class': 'form-select form-select-sm',
                                                    'aria-label': 'Small select example'})
        self.fields['recipients'].widget.attrs.update({'class': 'form-select form-select-sm',
                                                      'aria-label': 'Small select example'})
