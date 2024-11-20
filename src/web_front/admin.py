from django.contrib import admin
from web_front.models import Customer, Property, Memo, Job, Invoice, Constants
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

class JobInline(admin.TabularInline):
    model = Job
    extra = 0
    readonly_fields = ('created_at', 'updated_at')
    fields = ('title', 'status', 'pavement_type', 'estimated_value', 'job_done')

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('address', 'city', 'state', 'zip_code', 'customer')
    search_fields = ('address', 'city', 'state', 'zip_code', 'customer__first_name', 'customer__last_name')
    inlines = [JobInline]

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'is_active')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('is_active',)
    inlines = [JobInline]

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'customer', 'property', 'status', 'pavement_type', 'estimated_value', 'job_done')
    list_filter = ('status', 'pavement_type', 'job_done')
    search_fields = ('title', 'customer__first_name', 'customer__last_name', 'property__address')
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('photos',)

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'job', 'amount', 'paid', 'created_at')
    search_fields = ('job__title',)
    list_filter = ('paid', 'created_at')

@admin.register(Constants)
class ConstantsAdmin(admin.ModelAdmin):
    list_display = ('minimum_seal_price', 'base_seal_square_footage', 'seal_price', 'patch_price', 'caulk_price')

@admin.register(Memo)
class MemoAdmin(admin.ModelAdmin):
    list_display = ('property', 'content', 'created_at')
    search_fields = ('property__address', 'content')
    readonly_fields = ('created_at', 'updated_at')

def setup_user_roles():
    admin_group, created = Group.objects.get_or_create(name='Admin')
    manager_group, created = Group.objects.get_or_create(name='Manager')
    staff_group, created = Group.objects.get_or_create(name='Staff')

    # Assign permissions to Admin
    admin_permissions = Permission.objects.all()
    admin_group.permissions.set(admin_permissions)

    # Assign specific permissions to Manager
    manager_permissions = Permission.objects.filter(content_type__app_label='web_front', codename__in=[
        'add_job', 'change_job', 'view_job',
        'add_lead', 'change_lead', 'view_lead',
        'add_invoice', 'change_invoice', 'view_invoice',
    ])
    manager_group.permissions.set(manager_permissions)

    # Assign limited permissions to Staff
    staff_permissions = Permission.objects.filter(content_type__app_label='web_front', codename__in=[
        'view_job', 'view_lead', 'view_invoice',
    ])
    staff_group.permissions.set(staff_permissions)
