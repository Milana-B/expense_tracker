from django.contrib import admin
from expense_app.models import PaymentMethod, ExpenseCategory, ExpenseRecord

# Register your models here.

admin.site.register(PaymentMethod)
admin.site.register(ExpenseCategory)
admin.site.register(ExpenseRecord)
