import os
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from web_front.models import CustomerModel, PropertyModel, MemoModel

# Create your views here.

def index(request):
    # return render(request, 'web_front/index.html')
    # return HttpResponse('Hello, world. You\'re at the web_front index.')
    return render(request, 'index.html')

# def help(request):
#     # return render(request, 'web_front/help.html')
#     pass

# def customers(request):
#     # return render(request, 'web_front/customers.html')
#     pass

# def properties(request):
#     # return render(request, 'web_front/properties.html')
#     pass

# class new_cust(LoginRequiredMixin, CreateView):
#     model = CustomerModel
#     fields = ['last_name', 'first_name', 'email', 'phone_number', 'alt_phone_number']
#     success_url = reverse_lazy('customers')
    
# class edit_cust(LoginRequiredMixin, UpdateView):
#     model = CustomerModel
#     fields = ['last_name', 'first_name', 'email', 'phone_number', 'alt_phone_number']
#     success_url = reverse_lazy('customers')
    
# class new_prop(LoginRequiredMixin, CreateView):
#     model = PropertyModel
#     fields = ['customer', 'address', 'city', 'state', 'zip_code', 'seal_date', 'seal_square_footage', 'seal_quote', 'patch_date', 'patch_square_footage', 'patch_quote', 'caulk_date', 'caulk_square_footage', 'caulk_quote']
#     success_url = reverse_lazy('properties')
    
# class edit_prop(LoginRequiredMixin, UpdateView):
#     model = PropertyModel
#     fields = ['customer', 'address', 'city', 'state', 'zip_code', 'seal_date', 'seal_square_footage', 'seal_quote', 'patch_date', 'patch_square_footage', 'patch_quote', 'caulk_date', 'caulk_square_footage', 'caulk_quote']
#     success_url = reverse_lazy('properties')
    
# class new_memo(LoginRequiredMixin, CreateView):
#     model = MemoModel
#     fields = ['property', 'memo_field']
#     success_url = reverse_lazy('properties')
    
# class edit_memo(LoginRequiredMixin, UpdateView):
#     model = MemoModel
#     fields = ['property', 'memo_field']
#     success_url = reverse_lazy('properties')
    
# class delete_cust(LoginRequiredMixin, DeleteView):
#     model = CustomerModel
#     success_url = reverse_lazy('customers')
    
# class delete_prop(LoginRequiredMixin, DeleteView):
#     model = PropertyModel
#     success_url = reverse_lazy('properties')
    
# class delete_memo(LoginRequiredMixin, DeleteView):
#     model = MemoModel
#     success_url = reverse_lazy('properties')
    