from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import (
    TemplateView, ListView, CreateView, UpdateView, DetailView
)
from django.urls import reverse_lazy
from .models import Customer, Property, Job, Lead
from .forms import JobForm, LeadForm
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .services.analytics import LeadAnalyticsService

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
        return Job.objects.select_related('customer', 'property').all()

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

class LeadCreateView(LoginRequiredMixin, CreateView):
    model = Lead
    form_class = LeadForm
    template_name = 'web_front/new_lead.html'
    success_url = reverse_lazy('leads')

    def form_valid(self, form):
        lead = form.save(commit=False)
        lead.created_by = self.request.user
        lead.updated_by = self.request.user
        lead.save()
        messages.success(self.request, 'Lead created successfully!')
        return super().form_valid(form)

class LeadListView(LoginRequiredMixin, ListView):
    model = Lead
    template_name = 'web_front/leads.html'
    context_object_name = 'leads'
    paginate_by = 20

    def get_queryset(self):
        return Lead.objects.all()

class LeadDetailView(LoginRequiredMixin, DetailView):
    model = Lead
    template_name = 'web_front/lead_detail.html'
    context_object_name = 'lead'

class LeadUpdateView(LoginRequiredMixin, UpdateView):
    model = Lead
    form_class = LeadForm
    template_name = 'web_front/edit_lead.html'
    success_url = reverse_lazy('leads')

    def form_valid(self, form):
        lead = form.save(commit=False)
        lead.updated_by = self.request.user
        lead.save()
        messages.success(self.request, 'Lead updated successfully!')
        return super().form_valid(form)

class LeadDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'web_front/lead_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get analytics for different time periods
        context['monthly_stats'] = LeadAnalyticsService.get_lead_statistics(30)
        context['weekly_stats'] = LeadAnalyticsService.get_lead_statistics(7)
        context['yearly_stats'] = LeadAnalyticsService.get_lead_statistics(365)

        # Get recent leads
        context['recent_leads'] = Lead.objects.recent_leads(7)

        # Get overdue follow-ups
        context['overdue_leads'] = Lead.objects.filter(
            status='contacted',
            created_at__lt=timezone.now() - timedelta(days=2)
        )

        return context
