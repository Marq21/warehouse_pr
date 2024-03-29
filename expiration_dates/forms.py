from django import forms
from expiration_dates.models import ExpirationDateEntity


class AddExpirationDatesEntityForm(forms.ModelForm):

    class Meta:
        model = ExpirationDateEntity
        fields = ['name', 'nomenclature_remain',
                  'quantity', 'date_of_manufacture',
                  'date_of_expiration']
        widgets = {
            'name': forms.HiddenInput(),
            'date_of_manufacture': forms.TextInput(attrs={'class': 'form-field', 'type': 'date'}),
            'date_of_expiration': forms.TextInput(attrs={'class': 'form-field', 'type': 'date'}),
        }
        labels = {
            'nomenclature_remain': 'Срок для номенклатуры',
            'name': '',
        }


class LimitToExpirationDateForm(forms.Form):
    days_to_expiration = forms.IntegerField(
        initial=20, label="Введите количество дней до истечения срока годности")

class ExpiredGoodsForm(forms.Form):
    ...