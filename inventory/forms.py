from django import forms

from catalog.models import Category
from inventory.models import InventoryTask


class CreateInventoryTaskForm(forms.ModelForm):

    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label=None)

    class Meta:
        model = InventoryTask
        fields = ['name', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
        }
        labels = {
            'name': 'Название инвентаризации',
        }