from django import forms
from .models import Expense, Budget, Category

class ExpenseForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Expense
        fields = ['category', 'name', 'amount', 'date']

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'amount']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class ExpenseFilterForm(forms.Form):
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)