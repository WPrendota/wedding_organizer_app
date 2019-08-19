from __future__ import unicode_literals
from django import forms
from .models import Wedding, Table, Guest


class WeddingForm(forms.ModelForm):

    class Meta:
        model = Wedding
        fields = ['hall_name', 'date', 'city',]


class TableForm(forms.ModelForm):

    class Meta:
        model = Table
        fields = ['number', 'max_size', 'wedding',]

    def __init__(self, user, *args, **kwargs):
        super(TableForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['wedding'].queryset = Wedding.objects.filter(user=user)


class GuestForm(forms.ModelForm):

    class Meta:
        model = Guest
        fields = ['title', 'first_name', 'second_name', 'chair_number', 'family_side', 'wedding', 'table',]

    def __init__(self, user, *args, **kwargs):
        super(GuestForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['wedding'].queryset = Wedding.objects.filter(user=user)
            self.fields['table'].queryset = Table.objects.filter(user=user)
