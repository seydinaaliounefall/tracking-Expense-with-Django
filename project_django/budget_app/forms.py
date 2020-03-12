from django import forms

class BudgetForm(forms.Form):
    title = forms.CharField()
    amount = forms.IntegerField()