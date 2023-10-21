from web_front import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    # path('help', views.help, name='help'),
    # path('customers', views.customers, name='customers'),
    # path('properties', views.properties, name='properties'),
    # path('newcust', views.new_cust.as_view(), name='new_cust'),
    # path('newprop', views.new_prop.as_view(), name='new_prop'),
    # path('newmemo', views.new_memo.as_view(), name='new_memo'),
    # path('editcust/<customer_id>', views.edit_cust.as_view(), name='edit_cust'),
    # path('editprop/<property_id>', views.edit_prop.as_view(), name='edit_prop'),
    # path('editmemo/<memo_id>', views.edit_memo.as_view(), name='edit_memo'),
    # path('deletecust/<customer_id>', views.delete_cust.as_view(), name='delete_cust'),
    # path('deleteprop/<property_id>', views.delete_prop.as_view(), name='delete_prop'),
    # path('deletememo/<memo_id>', views.delete_memo.as_view(), name='delete_memo'),
]

