# forms.py
from django import forms
from .models import Supplier, Brand, Equipment

class PriceListForm(forms.Form):
    file = forms.FileField()

    supplier = forms.ModelChoiceField(queryset=Supplier.objects.all(), required=False)
    brand = forms.ModelChoiceField(queryset=Brand.objects.all(), required=False)
    equipment = forms.ModelChoiceField(queryset=Equipment.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        suppliers = kwargs.pop('suppliers', None)
        brands = kwargs.pop('brands', None)
        equipment = kwargs.pop('equipment', None)
        super(PriceListForm, self).__init__(*args, **kwargs)

        if suppliers is not None:
            self.fields['supplier'].queryset = suppliers
        if brands is not None:
            self.fields['brand'].queryset = brands
        if equipment is not None:
            self.fields['equipment'].queryset = equipment
