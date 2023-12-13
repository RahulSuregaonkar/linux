from .models import ReturnPolicy
from django import forms


class ReturnPolicyForm(forms.ModelForm):
    class Meta:
        model = ReturnPolicy
        fields = ['return_reason', 'refund_amount']

        widgets = {
            'return_reason': forms.Textarea(attrs={'rows': 4}),
            'refund_amount': forms.NumberInput(attrs={'step': '0.01'}),
        }