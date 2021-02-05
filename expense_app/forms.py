from django import forms
from django.contrib.auth.models import User
from .models import ExpenseRecord, PaymentMethod, ExpenseCategory
import datetime


def get_months():
    months = [('January', 'January'),
              ('February', 'February'),
              ('March', 'March'),
              ('April', 'April'),
              ('May', 'May'),
              ('June', 'June'),
              ('July', 'July'),
              ('August', 'August'),
              ('September', 'September'),
              ('October', 'October'),
              ('November', 'November'),
              ('December', 'December')]

    return months


def get_years():
    years = [(str(i), i) for i in range(2020, 2030)]

    return years


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ['username', 'email', 'password']


class DateForm(forms.Form):
    months = get_months()
    years = get_years()

    now = datetime.datetime.now()
    month = now.month
    year = now.year

    month = forms.ChoiceField(choices=months, initial=months[month - 1],
                              widget=forms.Select(attrs={'onChange': 'submit();'}))
    year = forms.ChoiceField(choices=years, initial=(str(year), year),
                             widget=forms.Select(attrs={'onChange': 'submit();'}))


class ExpenseRecordForm(forms.ModelForm):
    years = [i for i in range(2020, 2030)]
    date = forms.DateField(widget=forms.SelectDateWidget(years=years), initial=datetime.date.today)

    def __init__(self,*args,**kwargs):
        user = kwargs.pop('user')
        super(ExpenseRecordForm, self).__init__(*args, **kwargs)
        self.fields['payment_method'].queryset = PaymentMethod.objects.filter(user=user)
        self.fields['expense_category'].queryset = ExpenseCategory.objects.filter(user=user)

    class Meta():
        model = ExpenseRecord
        fields = ['date', 'amount', 'payments', 'payment_method', 'expense_category', 'note']


class PaymentMethodForm(forms.ModelForm):
    class Meta():
        model = PaymentMethod
        fields = ['name']


class ExpenseCategoryForm(forms.ModelForm):
    class Meta():
        model = ExpenseCategory
        fields = ['name']


class FilterDataForm(forms.Form):
    months = get_months()
    years = get_years()

    now = datetime.datetime.now()
    month = now.month
    year = now.year

    month = forms.ChoiceField(choices=months, initial=months[month - 1],
                              widget=forms.Select(attrs={'onChange': 'submit();'}))
    year = forms.ChoiceField(choices=years, initial=(str(year), year),
                             widget=forms.Select(attrs={'onChange': 'submit();'}))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(FilterDataForm, self).__init__(*args, **kwargs)

        payment_methods_query = PaymentMethod.objects.filter(user=self.user)
        expense_categories_query = ExpenseCategory.objects.filter(user=self.user)

        payment_methods_list = [(record.name, record.name) for record in payment_methods_query]
        expense_categories_list = [(record.name, record.name) for record in expense_categories_query]

        self.fields['payment_method'] = forms.MultipleChoiceField(
            choices=payment_methods_list,
            label="Payment Method",
            widget=forms.CheckboxSelectMultiple(attrs={'onChange': 'submit();'}),
            required=False)

        self.fields['expense_category'] = forms.MultipleChoiceField(
            choices=expense_categories_list,
            label="Expense Category",
            widget=forms.CheckboxSelectMultiple(attrs={'onChange': 'submit();'}),
            required=False)
