from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import (
    TemplateView, ListView, CreateView, UpdateView, DetailView
)
from django.urls import reverse_lazy
from .models import Customer, Property, Job, Lead, Invoice
from .forms import JobForm, ConstantsForm, LeadForm, InvoiceForm
from django.contrib import messages
from django.db import models
from django.db.models import Count, Sum
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
import logging

logger = logging.getLogger('web_front')

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'web_front/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customers = Customer.objects.filter(is_active=True)
        context['customers'] = customers
        context['total_customers'] = customers.count()
        return context

class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer
    template_name = 'web_front/customer_list.html'
    context_object_name = 'customers'
    paginate_by = 25

class JobListView(LoginRequiredMixin, ListView):
    model = Job
    template_name = 'web_front/jobs.html'
    context_object_name = 'jobs'
    paginate_by = 20

    def get_queryset(self):
        queryset = Job.objects.select_related('customer', 'property').all()
        pavement_type = self.request.GET.get('pavement_type')
        status = self.request.GET.get('status')
        search_query = self.request.GET.get('search')

        if pavement_type and pavement_type != 'all':
            queryset = queryset.filter(pavement_type=pavement_type)
        if status and status != 'all':
            queryset = queryset.filter(status=status)
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)

        return queryset

class JobDetailView(LoginRequiredMixin, DetailView):
    model = Job
    template_name = 'web_front/job.html'
    context_object_name = 'job'

class JobCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Job
    form_class = JobForm
    template_name = 'web_front/newjob.html'
    success_url = reverse_lazy('jobs')
    permission_required = 'web_front.add_job'

    def form_valid(self, form):
        job = form.save(commit=False)
        job.created_by = self.request.user
        job.updated_by = self.request.user
        job.save()
        form.save_m2m()
        logger.info(f"Job created: {job.title} by {self.request.user.username}")
        messages.success(self.request, 'Job created successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)

class JobUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Job
    form_class = JobForm
    template_name = 'web_front/editjob.html'
    success_url = reverse_lazy('jobs')
    permission_required = 'web_front.change_job'

    def form_valid(self, form):
        job = form.save(commit=False)
        job.updated_by = self.request.user
        job.save()
        form.save_m2m()
        messages.success(self.request, 'Job updated successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)

class LeadListView(LoginRequiredMixin, ListView):
    model = Lead
    template_name = 'web_front/leads.html'
    context_object_name = 'leads'
    paginate_by = 20

    def get_queryset(self):
        queryset = Lead.objects.all()
        status = self.request.GET.get('status')
        source = self.request.GET.get('source')
        search_query = self.request.GET.get('search')

        if status and status != 'all':
            queryset = queryset.filter(status=status)
        if source and source != 'all':
            queryset = queryset.filter(source=source)
        if search_query:
            queryset = queryset.filter(
                models.Q(first_name__icontains=search_query) |
                models.Q(last_name__icontains=search_query) |
                models.Q(email__icontains=search_query)
            )

        return queryset

class LeadDetailView(LoginRequiredMixin, DetailView):
    model = Lead
    template_name = 'web_front/lead_detail.html'
    context_object_name = 'lead'

class LeadCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Lead
    form_class = LeadForm
    template_name = 'web_front/new_lead.html'
    success_url = reverse_lazy('leads')
    permission_required = 'web_front.add_lead'

    def form_valid(self, form):
        lead = form.save(commit=False)
        lead.created_by = self.request.user
        lead.updated_by = self.request.user
        lead.save()
        messages.success(self.request, 'Lead created successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)

class LeadUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Lead
    form_class = LeadForm
    template_name = 'web_front/edit_lead.html'
    success_url = reverse_lazy('leads')
    permission_required = 'web_front.change_lead'

    def form_valid(self, form):
        lead = form.save(commit=False)
        lead.updated_by = self.request.user
        lead.save()
        messages.success(self.request, 'Lead updated successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)

class InvoiceCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = 'web_front/new_invoice.html'
    success_url = reverse_lazy('invoices')
    permission_required = 'web_front.add_invoice'

    def form_valid(self, form):
        invoice = form.save(commit=False)
        invoice.created_by = self.request.user
        invoice.updated_by = self.request.user
        invoice.save()
        form.save_m2m()
        messages.success(self.request, 'Invoice created successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)

class ReportingView(LoginRequiredMixin, TemplateView):
    template_name = 'web_front/reporting.html'

    @method_decorator(cache_page(60 * 15))  # Cache for 15 minutes
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_jobs'] = Job.objects.count()
        context['completed_jobs'] = Job.objects.filter(status='completed').count()
        context['total_estimated_value'] = Job.objects.aggregate(total=Sum('estimated_value'))['total'] or 0
        context['leads_count'] = Lead.objects.count()
        context['invoices_total'] = Invoice.objects.aggregate(total=Sum('amount'))['total'] or 0
        context['invoices_paid'] = Invoice.objects.filter(paid=True).aggregate(total=Sum('amount'))['total'] or 0
        return context
