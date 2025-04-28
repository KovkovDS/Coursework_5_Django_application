from django import forms
from .models import MailingRecipient
from django.core.exceptions import ValidationError


class MailingRecipientForm(forms.ModelForm):
    class Meta:
        model = MailingRecipient
        fields = ['initials', 'email', 'comment']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        cleaned_article_pk = self.instance.pk

        if MailingRecipient.objects.filter(email=email).exclude(id=cleaned_article_pk).exists():
            raise ValidationError('Статья с таким названием уже существует.')
        return email

    def __init__(self, *args, **kwargs):
        super(MailingRecipientForm, self).__init__(*args, **kwargs)
        self.fields['initials'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите Ф.И.О. клиента'})
        self.fields['email'].widget.attrs.update({'class': 'form-control',
                                                  'placeholder': 'Введите рабочий адрес электронной почты клиента'})
        self.fields['comment'].widget.attrs.update({'class': 'form-control', 'id': "exampleFormControlTextarea1",
                                                    'rows': "4", 'placeholder':
                                                        'Введите комментарий (описание) по данному клиенту'})
