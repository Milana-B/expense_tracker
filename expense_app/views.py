from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.db import models, IntegrityError

# Extra Imports for the Login and Logout Capabilities
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import PaymentMethod, ExpenseCategory, ExpenseRecord
from .forms import NewExpenseForm, DateForm, NewPaymentMethodForm, NewExpenseCategoryForm, FilterDataForm, UserForm
import datetime
import xlwt


# Create your views here.

# ExpenseRecord Model - Create, Update and Delete
class ExpenseRecordCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = NewExpenseForm
    model = ExpenseRecord

    def get_form_kwargs(self):
        kwargs = super(ExpenseRecordCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ExpenseRecordCreateView, self).form_valid(form)


class ExpenseRecordUpdateView(LoginRequiredMixin, generic.UpdateView):
    form_class = NewExpenseForm
    model = ExpenseRecord

    def get_form_kwargs(self):
        kwargs = super(ExpenseRecordUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class ExpenseRecordDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = ExpenseRecord
    success_url = reverse_lazy("expense_app:index")


# PaymentMethod Model - Create, Update and Delete
class PaymentMethodCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = NewPaymentMethodForm
    model = PaymentMethod

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(PaymentMethod, self).form_valid(form)


class PaymentMethodUpdateView(LoginRequiredMixin, generic.UpdateView):
    form_class = NewPaymentMethodForm
    model = PaymentMethod


class PaymentMethodDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = PaymentMethod
    success_url = reverse_lazy("expense_app:preferences")


# ExpenseCategory Model - Create, Update and Delete
class ExpenseCategoryCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = NewExpenseCategoryForm
    model = ExpenseCategory

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ExpenseCategory, self).form_valid(form)


class ExpenseCategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    form_class = NewExpenseCategoryForm
    model = ExpenseCategory


class ExpenseCategoryDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = ExpenseCategory
    success_url = reverse_lazy("expense_app:preferences")


@login_required()
def index(request):
    months_dict = dict(January=1, February=2, March=3, April=4, May=5, June=6,
                       July=7, August=8, September=9, October=10, November=11, December=12)

    now = datetime.datetime.now()
    month = now.month
    year = now.year

    form = DateForm()
    if request.method == 'POST':
        form = DateForm(request.POST)
        if form.is_valid():
            month_str = form.cleaned_data['month']
            month = months_dict[month_str]
            year = form.cleaned_data['year']

    user = request.user

    sum_dict = ExpenseRecord.objects.filter(date__month=month, date__year=year, user=user).aggregate(
        models.Sum('amount'))
    total_sum = sum_dict['amount__sum']

    expense_record_list = ExpenseRecord.objects.filter(date__month=month, date__year=year, user=user).order_by('date')

    context_dict = {'amount_sum': total_sum, 'expense_record': expense_record_list, 'form': form}

    return render(request, 'expense_app/index.html', context=context_dict)


@login_required()
def preferences(request):
    user = request.user
    payment_methods_list = PaymentMethod.objects.filter(user=user).order_by('name')
    expense_categories_list = ExpenseCategory.objects.filter(user=user).order_by('name')

    expense_category_form = NewExpenseCategoryForm()
    payment_method_form = NewPaymentMethodForm()

    if request.method == "POST":
        if 'save_method' in request.POST:
            payment_method_form = NewPaymentMethodForm(request.POST)
            if payment_method_form.is_valid():
                payment_method_form.save(commit=False)
                try:
                    payment_method_form.instance.user = request.user
                    payment_method_form.save(commit=True)
                except IntegrityError as e:
                    pass
                return HttpResponseRedirect(request.path)
            else:
                print("ERROR FORM INVALID")
        if 'save_category' in request.POST:
            expense_category_form = NewExpenseCategoryForm(request.POST)
            if expense_category_form.is_valid():
                expense_category_form.save(commit=False)
                try:
                    expense_category_form.instance.user = request.user
                    expense_category_form.save(commit=True)
                except IntegrityError as e:
                    pass
                return HttpResponseRedirect(request.path)
            else:
                print("ERROR FORM INVALID")

    context_dict = {'payment_methods_list': payment_methods_list, 'expense_categories_list': expense_categories_list,
                    'payment_method_form': payment_method_form, 'expense_category_form': expense_category_form}

    return render(request, 'expense_app/preferences.html', context_dict)


@login_required()
def filter(request):
    months_dict = dict(January=1, February=2, March=3, April=4, May=5, June=6,
                       July=7, August=8, September=9, October=10, November=11, December=12)

    now = datetime.datetime.now()
    month = now.month
    year = now.year

    expense_category = []
    payment_method = []
    form = FilterDataForm(user=request.user)

    if request.method == 'POST':
        form = FilterDataForm(request.POST, user=request.user)
        if form.is_valid():
            month_str = form.cleaned_data['month']
            month = months_dict[month_str]
            year = form.cleaned_data['year']
            payment_method = form.cleaned_data['payment_method']
            expense_category = form.cleaned_data['expense_category']

    user = request.user

    expense_record_list = ExpenseRecord.objects.filter(date__month=month, date__year=year, user=user,
                                                       expense_category__name__in=expense_category,
                                                       payment_method__name__in=payment_method).order_by('date')

    sum_dict = expense_record_list.aggregate(models.Sum('amount'))
    total_sum = sum_dict['amount__sum']

    context_dict = {'expense_record': expense_record_list, 'form': form, 'total_sum': total_sum}

    return render(request, 'expense_app/filter.html', context=context_dict)


@login_required()
def export_expense_records_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="expense_records.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('expense_records')
    ws.col(4).width = 5120
    ws.col(5).width = 5120

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Date', 'User', 'Amount', 'Payments', 'Payment Method', 'Expense Category', 'Note']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    font_style_date = xlwt.XFStyle()
    font_style_date.num_format_str = 'D-MMM-YY'

    user = request.user
    expense_record = ExpenseRecord.objects.filter(user=user).order_by('date')

    rows = []
    for record in expense_record:
        for method in record.payment_method.all():
            payment_method = method.name

        for category in record.expense_category.all():
            expense_category = category.name

        rows.append((record.date,
                     record.user.username,
                     record.amount,
                     record.payments,
                     payment_method,
                     expense_category,
                     record.note))

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            if col_num == 0:
                ws.write(row_num, col_num, row[col_num], font_style_date)
            else:
                ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        # Check to see both forms are valid
        if user_form.is_valid():
            # Save User Form to Database
            user = user_form.save()

            # Hash the password
            user.set_password(user.password)

            # Update with Hashed password
            user.save()

            # Registration Successful!
            registered = True

            # The form was invalid
            print(user_form.errors)

    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = UserForm()

    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    return render(request, 'expense_app/registration.html', {'user_form': user_form, 'registered': registered})


def user_login(request):
    if request.method == 'POST':
        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)

        # If we have a user
        if user:
            # Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request, user)
                # Send the user back to some page.
                # In this case their homepage.
                return HttpResponseRedirect(reverse('index'))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    else:
        # Nothing has been provided for username or password.
        return render(request, 'expense_app/login.html', {})
