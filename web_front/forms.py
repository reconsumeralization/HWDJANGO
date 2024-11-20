import logging
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django.forms import inlineformset_factory
from web_front.models import (
    Customer,
    Property,
    Memo,
    Job,
    Invoice,
    Constants,
    RemediationNeededModel,
)

logger = logging.getLogger(__name__)


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
        self.helper = FormHelper(self)
        self.helper.form_tag = True
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
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe the job details...'}),
            'photos': forms.ClearableFileInput(attrs={'multiple': True}),
            'estimated_value': forms.NumberInput(attrs={'min': 0, 'step': '0.01'}),
            'job_seal_square_footage': forms.NumberInput(attrs={'min': 0}),
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
        foot = self.cleaned_data.get('job_seal_square_footage')
        if foot and foot < 0:
            raise forms.ValidationError("Seal square footage cannot be negative.")
        return foot


JobFormSet = inlineformset_factory(
    Customer,
    Job,
    form=JobForm,
    fields=['title', 'status', 'pavement_type', 'estimated_value'],
    extra=1,
    can_delete=True
)


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = (
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'alt_phone_number'
        )


class ExcelUploadForm(forms.Form):
    file = forms.FileField()

    def clean(self):
        cleaned_data = super().clean()
        uploaded_file = cleaned_data.get('file')
        if uploaded_file:
            logger.debug(f'Uploaded file name: {uploaded_file.name}')
            logger.debug(f'Uploaded file size: {uploaded_file.size}')
        return cleaned_data


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = '__all__'
        widgets = {
            'invoice_date': forms.widgets.DateInput(attrs={'type': 'date'}),
        }


class MemoForm(forms.ModelForm):
    class Meta:
        model = Memo
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(MemoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('memo_field', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
        )


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        # fields = '__all__'
        fields = ('address', 'city', 'state', 'zip_code', 'seal_square_footage', 'notes')

    def __init__(self, *args, **kwargs):
        super(PropertyForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = True
        self.helper.form_id = 'id-propertyForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('address', css_class='form-group col-md-8 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('city', css_class='form-group col-md-4 mb-0'),
                Column('state', css_class='form-group col-md-2 mb-0'),
                Column('zip_code', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('seal_square_footage', css_class='form-group col-md-2 mb-0'),
                Column('notes', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            ButtonHolder(
                Submit('submit', 'Submit')
            ),
        )
        # return self.helper.form


NewJobFormSet = inlineformset_factory(
    Property,
    Job,
    form=JobForm,
    fields = (
        'title',
        'status',
        'pavement_type',
        'estimated_value',
        'scheduled_date',
        'completion_date',
        'description',
        'photos',
        'job_done',
        'job_seal_square_footage',
    ),
    extra=1,
    can_delete=False,
    can_delete_extra=True
)

TestMemoFormSet = inlineformset_factory(
    Property,
    Memo,
    fields=('memo_field',),
    extra=1,
    can_delete=True
)

MemoFormSet = inlineformset_factory(
    Property,
    Memo,
    form=MemoForm,
    extra=1,
    can_delete=True,
    can_delete_extra=True
)

NewPropFormSet = inlineformset_factory(
    Customer,
    Property,
    form=PropertyForm,
    fields = ('address', 'city', 'state', 'zip_code', 'seal_square_footage', 'notes'),
    extra=1,
    can_delete=False,
    can_delete_extra=True
)

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
