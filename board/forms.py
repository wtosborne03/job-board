from .models import Message
from crispy_forms.layout import Layout, Field
from address.widgets import AddressWidget
from django import forms
from .models import JobListing, Message, Application
from crispy_forms.helper import FormHelper
from jsite.custom_form import CustomSubmit
from dal import autocomplete


class JobListingForm(forms.ModelForm):
    class Meta:
        model = JobListing
        fields = [
            'title', 'category', 'description', 'location', 'salary_min', 'salary_max',
            'employment_type', 'experience_level', 'education_required', 'skills_required',
            'benefits', 'application_url', 'application_instructions', 'hiring_process',
            'is_remote', 'remote_type', 'status', 'application_deadline'
        ]
        widgets = {
            'application_deadline': forms.DateInput(attrs={'type': 'date'}),
            'location': AddressWidget(attrs={'class': 'form-input flex flex-row mt-1 block w-full rounded-lg'}),
            'skills_required': autocomplete.ModelSelect2Multiple(url='skills-autocomplete'),
            'benefits': autocomplete.ModelSelect2Multiple(url='benefits-autocomplete'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('title'),
            Field('category'),
            Field('description'),
            Field('location'),
            Field('salary_min'),
            Field('salary_max'),
            Field('employment_type'),
            Field('experience_level'),
            Field('education_required'),
            Field('skills_required'),
            Field('benefits'),
            Field('application_url'),
            Field('application_instructions'),
            Field('hiring_process'),
            Field('is_remote'),
            Field('remote_type'),
            Field('status'),
            Field('application_deadline'),
            CustomSubmit('submit', 'Save')
        )


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['recipient', 'content']
        widgets = {
            'recipient': autocomplete.ModelSelect2(url='user-autocomplete')
        }

    def __init__(self, *args, **kwargs):
        parent = kwargs.pop('parent', None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('recipient', css_class='h-32 bg-blue-600'),
            Field('content', css_class='h-96'),
            CustomSubmit(
                'submit', 'Send')
        )
        if parent:
            self.fields['recipient'].initial = parent.sender
            self.fields['recipient'].widget.attrs['readonly'] = True
            self.instance.parent = parent
        if self.initial.get('recipient'):
            self.fields['recipient'].widget.attrs['readonly'] = True


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('content', css_class='h-96'),
            CustomSubmit(
                'submit', 'Reply')
        )
        self.fields['content'].label = False


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['cover_letter']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('cover_letter', css_class='h-96'),
            CustomSubmit('submit', 'Submit Application')
        )
