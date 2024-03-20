import logging
import os
from typing import Any
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from phonenumbers import parse, PhoneNumberFormat, NumberParseException, format_number
from web_front.models import (
    CustomerModel,
    PropertyModel,
    MemoModel,
    JobModel,
    RemediationNeededModel,
    ConstantsModel,
)
from web_front.forms import (
    PropertyForm, 
    CustomerForm, 
    NewPropFormSet, 
    NewJobFormSet, 
    MemoFormSet, 
    MemoForm, 
    JobForm, 
    ConstantsForm,
    ExcelUploadForm,
    BrokenContactForm,
)
from django.forms import modelformset_factory
from django.db.models import Q, Prefetch
# import all classes and functions from import_module.py in web_front/lib
from web_front.lib.import_module import *


logger = logging.getLogger(__name__)


def index(request):
    return render(request, 'index.html')


def help_menu(request):
    context = {
        'title': 'Help',
        'message': 'This is the help_menu page.',
        'welcome': 'Welcome to the help_menu page.'
    }
    return render(request, 'help_menu.html')


class DisplayCustomers(LoginRequiredMixin, ListView):
    model = CustomerModel
    paginate_by = 15
    ordering = ['last_name']
    template_name = 'customers.html'
    context_object_name = 'customers'
    success_url = reverse_lazy('customers')
    
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(last_name__icontains=query) |
                Q(first_name__icontains=query) |
                Q(email__icontains=query) |
                Q(phone_number__icontains=query) |
                Q(alt_phone_number__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type_of_customers'] = str(type(context['customers']))
        return context


@login_required
def display_properties(request):
    # Handle the search query
    query = request.GET.get('q')
    
    memos = MemoModel.objects.all()
    # properties = PropertyModel.objects.all()
    properties = PropertyModel.objects.prefetch_related(Prefetch('memos', queryset=memos))
    
    if query:
        properties = properties.filter(
            Q(customer__last_name__icontains=query) |
            Q(customer__first_name__icontains=query) |
            Q(address__icontains=query) |
            Q(city__icontains=query) |
            Q(state__icontains=query) |
            Q(zip_code__icontains=query) |
            Q(seal_date__icontains=query) |
            Q(seal_square_footage__icontains=query) |
            Q(seal_quote__icontains=query) |
            Q(patch_date__icontains=query) |
            Q(patch_square_footage__icontains=query) |
            Q(patch_quote__icontains=query) |
            Q(caulk_date__icontains=query) |
            Q(caulk_square_footage__icontains=query) |
            Q(caulk_quote__icontains=query)
        )
    # Handle pagination
    paginator = Paginator(properties, 5)
    page = request.GET.get('page')
    properties_on_page = paginator.get_page(page)
    
    context = {
        'properties': properties_on_page,
    }
    
    # print(properties.query)
    return render(request, 'properties.html', context)


class DisplayProperties(LoginRequiredMixin, ListView):
    model = PropertyModel
    paginate_by = 5
    ordering = ['customer__last_name']
    template_name = 'properties.html'
    context_object_name = 'properties'
    success_url = reverse_lazy('properties')
    
    def get_queryset(self):
        memos = MemoModel.objects.all()
        queryset = super().get_queryset().prefetch_related(Prefetch('memos', queryset=memos))
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(customer__last_name__icontains=query) |
                Q(customer__first_name__icontains=query) |
                Q(address__icontains=query) |
                Q(city__icontains=query) |
                Q(state__icontains=query) |
                Q(zip_code__icontains=query) |
                Q(seal_square_footage__icontains=query)
            )
        return queryset


class NewCustomer(LoginRequiredMixin, CreateView):
    model = CustomerModel
    form_class = CustomerForm
    template_name = 'newcust.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'Customer created successfully')
        return super().form_valid(form)
    
    success_url = reverse_lazy('customers')
    

class EditCustomer(LoginRequiredMixin, UpdateView):
    model = CustomerModel
    form_class = CustomerForm
    template_name = 'editcust.html'
    
    def get_object(self, queryset=None):
        customer_id = self.kwargs.get('customer_id')
        return get_object_or_404(CustomerModel, id=customer_id)
    
    def form_valid(self, form):
        messages.success(self.request, 'Customer updated successfully')
        return super().form_valid(form)
    
    success_url = reverse_lazy('customers')
    

class EditProperty(LoginRequiredMixin, UpdateView):
    model = PropertyModel
    form_class = PropertyForm
    template_name = 'editprop.html'
    success_url = reverse_lazy('properties')
    
    def get_object(self, queryset=None):
        property_id = self.kwargs.get('property_id')
        return get_object_or_404(PropertyModel, id=property_id)
    
    def get_context_data(self, **kwargs):
        context = super(EditProperty, self).get_context_data(**kwargs)
        context['properties'] = context['form']
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Property updated successfully')
        form.instance.save()
        response = super().form_valid(form)
        return response


class NewProperty(LoginRequiredMixin, CreateView):
    template_name = 'newprop.html'
    form_class = PropertyForm
    model = PropertyModel
    
    def get(self, request, *args, **kwargs):
        customers = CustomerModel.objects.order_by('last_name', 'first_name')
        formset = NewPropFormSet(queryset=PropertyModel.objects.none())
        return render(request, self.template_name, {'formset': formset, 'customers': customers})
    
    def post(self, request, *args, **kwargs):
        formset = NewPropFormSet(request.POST)
        if formset.is_valid():
            customer_id = request.POST.get('customer')
            if customer_id:
                customer = CustomerModel.objects.get(pk=customer_id)
                instances = formset.save(commit=False)
                for instance in instances:
                    instance.customer = customer
                    instance.save()
                messages.success(request, 'Property created successfully')
                return redirect(reverse_lazy('properties'))
            else:
                messages.error(request, 'No customer selected')
        return render(request, self.template_name, {'formset': formset})
    
    def form_valid(self, form):
        messages.success(self.request, 'Property added successfully')
        return super().form_valid(form)
    
    success_url = reverse_lazy('properties')

    
class About(View):
    template_name = 'about.html'
    
    def get(self, request):
        context = {
            'title': 'About',
            'message': 'This is the About Page.',
            'welcome': 'Welcome to the About page.'
        }
        return render(request, 'about.html', context)


class Contact(View):
    template_name = 'contact.html'
    
    def get(self, request):
        context = {
            'title': 'Contact',
            'message': 'This is the Contact Page.',
            'welcome': 'Welcome to the Contact page.'
        }
        return render(request, 'contact.html', context)


class DisplayJobs(LoginRequiredMixin, ListView):
    model = JobModel
    paginate_by = 5
    ordering = ['property__customer__last_name']
    template_name = 'jobs.html'
    context_object_name = 'jobs'
    success_url = reverse_lazy('jobs')
    
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(property__customer__last_name__icontains=query) |
                Q(property__customer__first_name__icontains=query) |
                Q(property__address__icontains=query) |
                Q(property__city__icontains=query) |
                Q(property__state__icontains=query) |
                Q(property__zip_code__icontains=query) |
                Q(job_seal_date__icontains=query) |
                Q(job_seal_quote__icontains=query) |
                Q(job_patch_date__icontains=query) |
                Q(job_patch_quote__icontains=query) |
                Q(job_caulk_date__icontains=query)
            )
        return queryset
    
    # def get(self, request):
    #     jobs = JobModel.objects.all()
    #     context = {
    #         'jobs': jobs,
    #     }
    #     return render(request, 'jobs.html', context)
    

class ViewJob(LoginRequiredMixin, View):
    model = JobModel
    template_name = 'job.html'
    context_object_name = 'job'
    
    def get(self, request, job_id):
        job = JobModel.objects.get(pk=job_id)
        context = {
            'job': job,
        }
        return render(request, 'job.html', context)

    
class EditJob(LoginRequiredMixin, UpdateView):
    model = JobModel
    form_class = JobForm
    template_name = 'editjob.html'
    success_url = reverse_lazy('jobs')
    
    def get_object(self, queryset=None):
        job_id = self.kwargs.get('job_id')
        return get_object_or_404(JobModel, pk=job_id)
    
    def get_context_data(self, **kwargs):
        context = super(EditJob, self).get_context_data(**kwargs)
        context['jobs'] = context['form']
        return context
    
    def form_valid(self, form):
        job = form.save(commit=False)
        
        # Default to 0 if the value is None
        # job_seal_quote = job.job_seal_quote if job.job_seal_quote is not None else 0
        # print(job.job_seal_quote)
        calculate = lambda x: 395 + 0.22 * (x - 1000) if x > 1000 else 395
        # instance.job_seal_quote = calculate(instance.job_seal_square_footage)
        # print(job.job_seal_square_footage)
        # print(job.job_seal_quote)
        # print(calculate(job.job_seal_square_footage))
        job_seal_quote = int(calculate(job.job_seal_square_footage))
        job_patch_quote = job.job_patch_quote if job.job_patch_quote is not None else 0
    
        job.job_total_quote = job_seal_quote + job_patch_quote
        job.job_seal_quote = job_seal_quote
        job.save()
        
        messages.success(self.request, 'Job updated successfully')
        # form.instance.save()
        return super().form_valid(form)


class NewJob(LoginRequiredMixin, CreateView):
    template_name = 'newjob.html'
    form_class = JobForm
    model = JobModel
    
    def get(self, request, *args, **kwargs):
        properties = PropertyModel.objects.order_by('customer__last_name', 'address')
        formset = NewJobFormSet(queryset=JobModel.objects.none())
        return render(request, self.template_name, {'formset': formset, 'properties': properties})
    
    def post(self, request, *args, **kwargs):
        formset = NewJobFormSet(request.POST)
        if formset.is_valid():
            property_id = request.POST.get('property')
            if property_id:
                property = PropertyModel.objects.get(pk=property_id)
                instances = formset.save(commit=False)
                for instance in instances:
                    if instance.job_seal_square_footage is not None:
                        calculate = lambda x: 1000 + 0.22 * (x - 1000) if x > 1000 else 1000
                        instance.job_seal_quote = calculate(instance.job_seal_square_footage)
                    instance.property = property
                    instance.save()
                messages.success(request, 'Job created successfully')
                return redirect(reverse_lazy('jobs'))
            else:
                messages.error(request, 'No property selected')
        else:
            print("formset is not valid", formset.errors)
            print("nonformset errors:", formset.non_form_errors())
            messages.error(request, 'Please correct the errors below.')
        return render(request, self.template_name, {'formset': formset})
    
    def form_valid(self, form):
        messages.success(self.request, 'Job added successfully')
        return super().form_valid(form)
    
    success_url = reverse_lazy('jobs')


class ImportCustomers(LoginRequiredMixin, FormView):
    """
    Import customers from an Excel spreadsheet.
    """
    template_name = 'excel_import.html'
    form_class = ExcelUploadForm
    success_url = reverse_lazy('import_customers')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['welcome_text'] = 'Importing Customers...'
        return context

    def form_valid(self, form):
        # create a new CustomersObjectSet object
        if form.is_valid():
            uploaded_file = form.cleaned_data['file']
            logger.info(f'Uploaded file name: {uploaded_file.name}')
            logger.info(f'Uploaded file size: {uploaded_file.size}')
        logger.debug(f"MEDIA_ROOT: {settings.MEDIA_ROOT}")
        file_path = os.path.join(settings.MEDIA_ROOT, 'uploaded_file.xlsx')
        logger.debug(f"file_path: {file_path}")
        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        import_file = CustomersObjectSet(file_path, self.request.user, self.request.user)
        imported_customers = import_customers(import_file)

        if imported_customers is None:
            messages.error(
                self.request,
                'An error occurred during the import process. Please check the file format and contents.'
            )
            return super().form_valid(form)

        error_messages = []
        # Create or update the customer in the CustomerModel
        for this_customer in imported_customers.customer_set:
            try:
                # Validate email
                email = this_customer['email']
                if email:
                    validate_email(email)

                # Validate phone number
                phone_number = self.format_phone_number(this_customer['phone'])
                alt_phone_number = self.format_phone_number(this_customer['alt_phone'])

                CustomerModel.objects.update_or_create(
                    last_name=this_customer['last_name'],
                    email=email,
                    defaults={
                        'first_name': this_customer['first_name'],
                        'phone_number': phone_number,
                        'alt_phone_number': alt_phone_number,
                        'created_by': this_customer['created_by'],
                        'updated_by': this_customer['updated_by'],
                    }
                )
            except (ValidationError, IntegrityError, NumberParseException) as e:
                error_message = f"Error importing {this_customer['first_name']} {this_customer['last_name']}: {e}\n"
                RemediationNeededModel.objects.update_or_create(
                    last_name=this_customer['last_name'],
                    email=this_customer['email'],
                    first_name=this_customer['first_name'],
                    phone_number=this_customer['phone'],
                    alt_phone_number=this_customer['alt_phone'],
                    created_by=this_customer['created_by'],
                    updated_by=this_customer['updated_by'],
                )
                logger.error(error_message)
                error_messages.append(error_message)
        if error_messages:
            error_message = "Some customers could not be imported:\n" + "\n".join(error_messages)
            messages.error(self.request, error_message)
        else:
            messages.success(self.request, 'Customers imported successfully')
        return super().form_valid(form)

    @staticmethod
    def format_phone_number(phone_number_str):
        if phone_number_str:
            try:
                logger.debug(f"phone_number_str: {phone_number_str}")
                phone_number_str = str(phone_number_str)
                phone_number = parse(phone_number_str, 'US')
                return format_number(phone_number, PhoneNumberFormat.E164)
            except NumberParseException as e:
                logger.error(f"Error parsing phone number: {e}")
                return None
        return None


# ------- broken contacts view ----------------
class BrokenContacts(LoginRequiredMixin, ListView):
    model = RemediationNeededModel
    paginate_by = 100
    ordering = ['last_name']
    template_name = 'broken_contacts.html'
    context_object_name = 'broken_contacts'
    success_url = reverse_lazy('broken_contacts')

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(last_name__icontains=query) |
                Q(first_name__icontains=query) |
                Q(email__icontains=query) |
                Q(phone_number__icontains=query)
            )
        return queryset


class EditBroken(LoginRequiredMixin, UpdateView):
    model = RemediationNeededModel
    form_class = BrokenContactForm
    template_name = 'editbroken.html'

    def get_object(self, queryset=None):
        broken_id = self.kwargs.get('broken_id')
        return get_object_or_404(RemediationNeededModel, id=broken_id)

    def form_valid(self, form):
        messages.success(self.request, 'Customer updated successfully')
        return super().form_valid(form)

    success_url = reverse_lazy('customers')

