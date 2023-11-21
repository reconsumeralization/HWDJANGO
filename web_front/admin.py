from django.contrib import admin
from web_front.models import CustomerModel, PropertyModel, MemoModel, JobModel, InvoiceModel, ConstantsModel

# Register your models here.
admin.site.register(CustomerModel)
admin.site.register(PropertyModel)
admin.site.register(MemoModel)
admin.site.register(JobModel)
admin.site.register(InvoiceModel)
admin.site.register(ConstantsModel)
