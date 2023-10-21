from django.contrib import admin
from web_front.models import CustomerModel, PropertyModel, MemoModel

# Register your models here.
admin.site.register(CustomerModel)
admin.site.register(PropertyModel)
admin.site.register(MemoModel)
