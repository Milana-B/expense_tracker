from django.urls import path
from expense_app import views


app_name = 'expense_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('preferences/', views.preferences, name='preferences'),
    path('filter/', views.filter, name='filter'),
    path('expense_record/create/',views.ExpenseRecordCreateView.as_view(), name='create_expense_record'),
    path('expense_record/update/<pk>',views.ExpenseRecordUpdateView.as_view(), name='update_expense_record'),
    path('expense_record/delete/<pk>',views.ExpenseRecordDeleteView.as_view(), name='delete_expense_record'),
    path('preferences/expense_category/update/<pk>', views.ExpenseCategoryUpdateView.as_view(), name='update_expense_category'),
    path('preferences/expense_category/delete/<pk>', views.ExpenseCategoryDeleteView.as_view(), name='delete_expense_category'),
    path('preferences/payment_method/update/<pk>', views.PaymentMethodUpdateView.as_view(), name='update_payment_method'),
    path('preferences/payment_method/delete/<pk>', views.PaymentMethodDeleteView.as_view(), name='delete_payment_method'),
    path('export/', views.export_expense_records_xls , name='export_expense_records_xls'),
    path('register/', views.register, name='register'),
    path('user_login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='logout'),
]
