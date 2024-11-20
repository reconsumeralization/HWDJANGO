from django.db import models
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        related_name="%(class)s_created"
    )
    updated_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        related_name="%(class)s_updated"
    )

    class Meta:
        abstract = True

class Customer(BaseModel):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(null=True, blank=True, unique=True)
    phone_number = PhoneNumberField(region='US')
    alt_phone_number = PhoneNumberField(null=True, blank=True, region='US')
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        indexes = [
            models.Index(fields=['last_name', 'first_name']),
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"

class Property(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='properties')
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=10)
    square_footage = models.PositiveIntegerField()
    notes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Properties"
        ordering = ['customer__last_name', 'address']

    def __str__(self):
        return f"{self.address}, {self.city}, {self.state}"

class Job(BaseModel):
    STATUS_CHOICES = [
        ('lead', 'Lead'),
        ('estimate', 'Estimate'),
        ('scheduled', 'Scheduled'),
        ('in-progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    PAVEMENT_TYPE_CHOICES = [
        ('driveway', 'Driveway'),
        ('parking_lot', 'Parking Lot'),
        ('private_road', 'Private Road'),
    ]

    title = models.CharField(max_length=100)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='jobs')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='jobs')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='lead')
    pavement_type = models.CharField(max_length=20, choices=PAVEMENT_TYPE_CHOICES)
    estimated_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    scheduled_date = models.DateField(null=True, blank=True)
    completion_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    photos = models.ManyToManyField('media.Media', blank=True)
    job_done = models.BooleanField(default=False)
    job_seal_square_footage = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.title} - {self.get_pavement_type_display()}"

    class Meta:
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['pavement_type']),
            models.Index(fields=['estimated_value']),
        ]
        ordering = ['-created_at']

class Invoice(BaseModel):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='invoices')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['paid']),
            models.Index(fields=['created_at']),
            models.Index(fields=['job']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"Invoice #{self.id} for {self.job.title}"

class Constants(BaseModel):
    minimum_seal_price = models.DecimalField(max_digits=10, decimal_places=2)
    base_seal_square_footage = models.PositiveIntegerField()
    seal_price = models.DecimalField(max_digits=10, decimal_places=2)
    patch_price = models.DecimalField(max_digits=10, decimal_places=2)
    caulk_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return "Constants"

class Memo(BaseModel):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='memos')
    content = models.TextField()

    def __str__(self):
        return f"Memo for {self.property.address}"

class Lead(BaseModel):
    SOURCE_CHOICES = [
        ('website', 'Website'),
        ('referral', 'Referral'),
        ('advertisement', 'Advertisement'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('qualified', 'Qualified'),
        ('converted', 'Converted'),
        ('unqualified', 'Unqualified'),
    ]

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField(region='US')
    source = models.CharField(max_length=50, choices=SOURCE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.get_status_display()}"
