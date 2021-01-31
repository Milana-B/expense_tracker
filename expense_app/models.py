from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.


class PaymentMethod(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=264)

    def get_absolute_url(self):
        return reverse("expense_app:preferences")

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('user', 'name')


class ExpenseCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=264)

    def get_absolute_url(self):
        return reverse("expense_app:preferences")

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('user', 'name')


class ExpenseRecord(models.Model):
    date_time = models.DateTimeField(auto_now_add=True, blank=True)
    date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    payments = models.IntegerField()
    payment_method = models.ManyToManyField(PaymentMethod)
    expense_category = models.ManyToManyField(ExpenseCategory)
    note = models.CharField(max_length=264)

    def get_absolute_url(self):
        return reverse("expense_app:index")

    def __str__(self):
        return str(self.date_time)
