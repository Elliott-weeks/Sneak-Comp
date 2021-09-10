from django.conf import settings
from django.db import models
from competitions.models import Competition


# Create your models here.

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null= True)
    item = models.ForeignKey(Competition, on_delete=models.CASCADE)
    answer = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)
    def __str__(self):
        return str(self.pk)
    def get_total_item_price(self):
        return self.quantity * self.item.price





class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address_line_1 = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=100)
    def __str__(self):
        return self.postal_code

class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    status = models.CharField(default="Failed", max_length=20)
    payee_email = models.EmailField()
    paypal_payment_id = models.CharField(max_length=100)
    paypal_payer_id = models.CharField(max_length=100)
    value = models.FloatField()
    currency_code = models.CharField(max_length=5)
    payment_date = models.DateField(auto_now_add=True)
    full_name = models.CharField(max_length=70)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    def __str__(self):
        return self.payee_email

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem, blank=True)
    start_date = models.DateTimeField(auto_now_add=True)
    order_date = models.DateTimeField()
    is_ordered = models.BooleanField(default=False)
    payment = models.OneToOneField(Payment, on_delete= models.RESTRICT, null=True, blank=True)
    def __str__(self):
        return str(self.pk)

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_item_price()
        return total



