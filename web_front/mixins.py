from django import forms
from django.contrib import messages
from django.core.exceptions import PermissionDenied

class AuditFormMixin:
    def save(self, commit=True):
        if not self.instance.pk:
            self.instance.created_by = self.request.user
        self.instance.updated_by = self.request.user
        return super().save(commit)

class PhoneNumberFormMixin:
    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if phone:
            # Remove any non-numeric characters
            phone = ''.join(filter(str.isdigit, str(phone)))
            if len(phone) != 10:
                raise forms.ValidationError("Phone number must be 10 digits")
        return phone

class UserContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_leads'] = Lead.objects.filter(created_by=self.request.user)
        context['user_jobs'] = Job.objects.filter(created_by=self.request.user)
        return context

class OwnershipRequiredMixin:
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.created_by != self.request.user:
            raise PermissionDenied("You don't have permission to access this object")
        return obj

class SuccessMessageMixin:
    success_message = ""

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.success_message:
            messages.success(self.request, self.success_message)
        return response
