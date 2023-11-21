from phonenumber_field.modelfields import PhoneNumberField
from django.db import models


# ------ a model for leads ----------------
class LeadsModel(models.Model):
    last_name = models.CharField(max_length=30, blank=False)
    first_name = models.CharField(max_length=30, blank=False)
    email = models.EmailField(null=True, max_length=254, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True, region='US')
    alt_phone_number = PhoneNumberField(null=True, blank=True, region='US')
    created_by = models.CharField(max_length=30, blank=True)
    updated_by = models.CharField(max_length=30, blank=True)
    lead_source = models.CharField(max_length=30, blank=True)
    subscribed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'


# ------ a model for customers ----------------
class CustomerModel(models.Model):
    last_name = models.CharField(max_length=30, blank=False)
    first_name = models.CharField(max_length=30, blank=False)
    email = models.EmailField(max_length=254, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True, region='US')
    alt_phone_number = PhoneNumberField(null=True, blank=True, region='US')
    created_by = models.CharField(max_length=30, blank=True)
    updated_by = models.CharField(max_length=30, blank=True)
    subscribed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'


# ------ a model for leads which need to be remediated ----------------
class RemediationNeededModel(models.Model):
    last_name = models.CharField(null=True, max_length=30, blank=False)
    first_name = models.CharField(null=True, max_length=30, blank=False)
    email = models.EmailField(null=True, max_length=254, blank=True)
    phone_number = models.CharField(null=True, blank=True)
    alt_phone_number = models.CharField(null=True, blank=True)
    created_by = models.CharField(max_length=30, blank=True)
    updated_by = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'



class PropertyModel(models.Model):
    customer = models.ForeignKey(CustomerModel, on_delete=models.CASCADE)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    zip_code = models.CharField(max_length=10)
    seal_square_footage = models.IntegerField(blank=False, null=False)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.customer.last_name}: {self.address}'


class MemoModel(models.Model):
    property = models.ForeignKey(PropertyModel, on_delete=models.CASCADE, related_name='memos')
    memo_field = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.property.customer.last_name}: {self.property.address}'


class JobModel(models.Model):
    property = models.ForeignKey(PropertyModel, on_delete=models.CASCADE, related_name='jobs')
    job_seal_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    job_seal_square_footage = models.IntegerField(blank=False, null=False, default=0)
    job_seal_quote = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=False)
    job_patch_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    job_patch_square_footage = models.IntegerField(blank=True, null=True)
    job_patch_quote = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    job_caulk_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    job_caulk_footage = models.IntegerField(blank=True, null=True)
    job_total_quote = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    job_notes = models.TextField(blank=True, null=True)
    job_done = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.job_seal_date}: {self.property.customer.last_name}: {self.job_total_quote}'


class InvoiceModel(models.Model):
    job = models.ForeignKey(JobModel, on_delete=models.CASCADE, related_name='invoices')
    invoice_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    invoice_total = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    invoice_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.invoice_date}: {self.job.property.customer.last_name}: {self.invoice_total}'


class ConstantsModel(models.Model):
    minimum_seal_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    base_seal_square_footage = models.IntegerField(blank=True, null=True)
    seal_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    patch_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    caulk_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f'Constants'
