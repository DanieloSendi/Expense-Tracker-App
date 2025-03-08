from django import forms
from .models import Expense, Budget

class ExpenseForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),  
        input_formats=["%Y-%m-%d"]
    )
    class Meta:
        model = Expense
        fields = ['category', 'amount', 'date', 'description']


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['amount']
        