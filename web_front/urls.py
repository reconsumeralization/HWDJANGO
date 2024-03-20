from web_front import views
from django.urls import path, include

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.About.as_view(), name='about'),
    path('contact', views.Contact.as_view(), name='contact'),
    path('help_menu', views.help_menu, name='help_menu'),
    path('customers', views.DisplayCustomers.as_view(), name='customers'),
    path('editcust/<int:customer_id>', views.EditCustomer.as_view(), name='edit_cust'),
    path('newcust', views.NewCustomer.as_view(), name='new_cust'),
    # path('deletecust/<customer_id>', views.delete_cust.as_view(), name='delete_cust'),
    path("__debug__/", include("debug_toolbar.urls")),
    # path('properties2', views.display_properties, name='properties'),
    path('properties', views.DisplayProperties.as_view(), name='properties'),
    path('editprop/<int:property_id>', views.EditProperty.as_view(), name='edit_prop'),
    path('newprop', views.NewProperty.as_view(), name='new_prop'),
    path('jobs', views.DisplayJobs.as_view(), name='jobs'),
    path('edit_job/<int:job_id>', views.EditJob.as_view(), name='edit_job'),
    path('newjob', views.NewJob.as_view(), name='new_job'),
    path('view_job/<int:job_id>', views.ViewJob.as_view(), name='view_job'),
    path('import_customers', views.ImportCustomers.as_view(), name='import_customers'),
    path('broken_contacts', views.BrokenContacts.as_view(), name='broken_contacts'),
    path('edit_broken/<int:broken_id>', views.EditBroken.as_view(), name='edit_broken'),
    # path('deleteprop/<property_id>', views.delete_prop.as_view(), name='delete_prop'),
    # path('newmemo', views.new_memo.as_view(), name='new_memo'),
    # path('editmemo/<memo_id>', views.edit_memo.as_view(), name='edit_memo'),
    # path('deletememo/<memo_id>', views.delete_memo.as_view(), name='delete_memo'),
]

