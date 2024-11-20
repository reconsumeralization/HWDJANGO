from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from .models import Job, Constants, Lead

class ConstantsForm(forms.ModelForm):
    class Meta:
        model = Constants
        fields = ('minimum_seal_price', 'base_seal_square_footage', 'seal_price', 'patch_price', 'caulk_price')
        widgets = {
            'minimum_seal_price': forms.NumberInput(attrs={'min': 0, 'step': '0.01'}),
            'base_seal_square_footage': forms.NumberInput(attrs={'min': 0}),
            'seal_price': forms.NumberInput(attrs={'min': 0, 'step': '0.01'}),
            'patch_price': forms.NumberInput(attrs={'min': 0, 'step': '0.01'}),
            'caulk_price': forms.NumberInput(attrs={'min': 0, 'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        super(ConstantsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'minimum_seal_price',
            'base_seal_square_footage',
            'seal_price',
            'patch_price',
            'caulk_price',
            Submit('submit', 'Save Constants', css_class='btn btn-primary')
        )

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            'title',
            'customer',
            'property',
            'status',
            'pavement_type',
            'estimated_value',
            'scheduled_date',
            'completion_date',
            'description',
            'photos',
            'job_done',
            'job_seal_square_footage',
        ]
        widgets = {
            'scheduled_date': forms.SelectDateWidget(),
            'completion_date': forms.SelectDateWidget(),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter job description here...'}),
            'photos': forms.ClearableFileInput(attrs={'multiple': True}),
        }

    def __init__(self, *args, **kwargs):
        super(JobForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'title',
            'customer',
            'property',
            'status',
            'pavement_type',
            'estimated_value',
            'scheduled_date',
            'completion_date',
            'description',
            'photos',
            'job_done',
            'job_seal_square_footage',
            Submit('submit', 'Save Job', css_class='btn btn-primary')
        )

    def clean_estimated_value(self):
        estimated_value = self.cleaned_data.get('estimated_value')
        if estimated_value and estimated_value < 0:
            raise forms.ValidationError("Estimated value cannot be negative.")
        return estimated_value

    def clean_job_seal_square_footage(self):
        footage = self.cleaned_data.get('job_seal_square_footage')
        if footage and footage < 0:
            raise forms.ValidationError("Seal square footage cannot be negative.")
        return footage

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'source', 'status', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Additional notes...'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Lead.objects.filter(email=email).exists():
            raise forms.ValidationError("A lead with this email already exists.")
        return email
