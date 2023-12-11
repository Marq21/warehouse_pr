from django import forms
from captcha.fields import CaptchaField


from .models import Nomenclature, Category, get_new_barcode


class CaptchaTestForm(forms.Form):
    captcha = CaptchaField()


class AddNomenclatureForm(forms.ModelForm):
    user = forms.CharField(widget=forms.HiddenInput(),
                           required=False, label='')

    class Meta:
        model = Nomenclature
        fields = ['name', 'weight_or_piece',
                  'barcode', 'cost',
                  'category', 'country_made',]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
        }
        labels = {
            'barcode': 'Штрих-код',
        }


class AddCategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
        }


class EmailNomenclatureForm(forms.Form):
    name = forms.CharField(max_length=50)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class SearchForm(forms.Form):
    query = forms.CharField()
