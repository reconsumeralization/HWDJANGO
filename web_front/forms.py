import logging
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, Row, Column, Field, Fieldset, ButtonHolder, Button, Hidden
from django.forms import inlineformset_factory
from web_front.models import (
    CustomerModel,
    PropertyModel,
    MemoModel,
    JobModel,
    InvoiceModel,
    ConstantsModel,
    RemediationNeededModel,
)

logger = logging.getLogger(__name__)


class ConstantsForm(forms.ModelForm):
    class Meta:
        model = ConstantsModel
        # fields = '__all__'
        fields = ('minimum_seal_price', 'base_seal_square_footage', 'seal_price', 'patch_price', 'caulk_price')

    def __init__(self, *args, **kwargs):
        super(ConstantsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = True
        self.helper.form_method = 'post'
        self.helper.form_class = 'blueForms'
        self.helper.form_id = 'id-constantsForm'


class BrokenContactForm(forms.ModelForm):
    class Meta:
        model = RemediationNeededModel
        fields = (
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'alt_phone_number'
        )


class CustomerForm(forms.ModelForm):
    class Meta:
        model = CustomerModel
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
        model = InvoiceModel
        fields = '__all__'
        widgets = {
            'invoice_date': forms.widgets.DateInput(attrs={'type': 'date'}),
        }


class JobForm(forms.ModelForm):
    class Meta:
        model = JobModel
        # fields = '__all__'
        fields = (
            'job_seal_date',
            'job_seal_square_footage',
            'job_seal_quote',
            'job_patch_date',
            'job_patch_square_footage',
            'job_patch_quote',
            'job_caulk_date',
            'job_caulk_footage',
            # 'job_total_quote',
            'job_notes',
            'job_done',
        )

    def __init__(self, *args, **kwargs):
        super(JobForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = True
        self.helper.form_id = 'id-jobForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.fields['job_seal_date'].widget = forms.DateInput(attrs={'type': 'date'})
        self.fields['job_patch_date'].widget = forms.DateInput(attrs={'type': 'date'})
        self.fields['job_caulk_date'].widget = forms.DateInput(attrs={'type': 'date'})
        self.fields['job_total_quote_readonly'] = forms.DecimalField(
            initial=self.instance.job_total_quote,
            disabled=True,
            required=False,
            label='Total Quote',
        )
        self.helper.layout = Layout(
            Row(
                Column('job_seal_date', css_class='form-group col-md-2 mb-0'),
                Column('job_seal_square_footage', css_class='form-group col-md-2 mb-0'),
                Hidden('job_seal_quote', 1000),
                Column('job_total_quote_readonly', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('job_patch_date', css_class='form-group col-md-2 mb-0'),
                Column('job_patch_square_footage', css_class='form-group col-md-2 mb-0'),
                Column('job_patch_quote', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('job_caulk_date', css_class='form-group col-md-2 mb-0'),
                Column('job_caulk_footage', css_class='form-group col-md-2 mb-0'),
                Column('job_done', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('job_notes', css_class='form-group col-md-6 mb-0'),
            ),
            ButtonHolder(
                Submit('submit', 'Submit')
            ),
        )


class MemoForm(forms.ModelForm):
    class Meta:
        model = MemoModel
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
        model = PropertyModel
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
    PropertyModel,
    JobModel,
    form=JobForm,
    fields = (
        'job_seal_date',
        'job_seal_square_footage',
        'job_seal_quote',
        'job_patch_date',
        'job_patch_square_footage',
        'job_patch_quote',
        'job_caulk_date',
        'job_caulk_footage',
        'job_notes',
        'job_done',
    ),
    extra=1,
    can_delete=False,
    can_delete_extra=True
)

TestMemoFormSet = inlineformset_factory(
    PropertyModel, 
    MemoModel, 
    fields=('memo_field',), 
    extra=1, 
    can_delete=True
)

MemoFormSet = inlineformset_factory(
    PropertyModel, 
    MemoModel, 
    form=MemoForm, 
    extra=1, 
    can_delete=True, 
    can_delete_extra=True
)

NewPropFormSet = inlineformset_factory(
    CustomerModel, 
    PropertyModel, 
    form=PropertyForm,
    fields = ('address', 'city', 'state', 'zip_code', 'seal_square_footage', 'notes'),
    extra=1, 
    can_delete=False, 
    can_delete_extra=True
)

