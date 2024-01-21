from django import forms

from catalog.models import Category, Nomenclature
from inventory.models import InventoryTask


class CreateInventoryTaskForm(forms.ModelForm):

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), empty_label=None)

    class Meta:
        model = InventoryTask
        fields = ['name', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
        }
        labels = {
            'name': 'Название инвентаризации',
        }


class InputBarcode(forms.Form):
    barcode_input = forms.CharField(
        min_length=1, max_length=200, label='Введите штрих-код ', required=False)
    
    def clean_barcode_input(self):
        barcode = self.cleaned_data['barcode_input']
        if not Nomenclature.objects.filter(barcode=barcode).exists():
            raise forms.ValidationError("Штрих-код отсутсвует в базе данных")
        return barcode
    

class UpdateStatus(forms.Form):
    inventory_task_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)