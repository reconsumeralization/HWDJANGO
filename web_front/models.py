from phonenumber_field.modelfields import PhoneNumberField
from django.db import models


class CustomerModel(models.Model):
    last_name = models.CharField(max_length=30, blank=False)
    first_name = models.CharField(max_length=30, blank=False)
    email = models.EmailField(max_length=254, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True, region='US')
    alt_phone_number = PhoneNumberField(null=True, blank=True, region='US')
    
    def __str__(self):
        return f'{self.last_name}, {self.first_name}'
    
    
    
class PropertyModel(models.Model):
    customer = models.ForeignKey(CustomerModel, on_delete=models.CASCADE)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    zip_code = models.CharField(max_length=10)
    seal_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    seal_square_footage = models.IntegerField(blank=False, null=False)
    seal_quote = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    patch_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    patch_square_footage = models.IntegerField(blank=True, null=True)
    patch_quote = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    caulk_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    caulk_square_footage = models.IntegerField(blank=True, null=True)
    caulk_quote = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    def __str__(self):
        return f'{self.customer.last_name}: {self.address}'
    
class MemoModel(models.Model):
    property = models.ForeignKey(PropertyModel, on_delete=models.CASCADE)
    memo_field = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.property.customer.last_name}: {self.property.address}'