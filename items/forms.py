from django import forms

from items.models import Item


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['articul', 'price', 'count', 'discount']
        widget = {
            'articul': forms.TextInput(),
            'price': forms.NumberInput(),
            'count': forms.NumberInput(),
            'discount': forms.NumberInput(attrs={})
        }
