from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from jsite.custom_form import CustomSubmit
from .models import EmployerProfile, JobSeekerProfile, UserProfile
from django.contrib.auth.forms import AuthenticationForm
from jsite.custom_form import ImagePreviewWidget
from dal import autocomplete


class CustomUserCreationForm(UserCreationForm):
    ACCOUNT_CHOICES = [
        ('employer', 'Employer'),
        ('job_seeker', 'Job Seeker'),
    ]

    user_type = forms.ChoiceField(
        choices=ACCOUNT_CHOICES, widget=forms.RadioSelect, required=True)

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'user_type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('email'),
            Field('password1'),
            Field('password2'),
            Field('user_type'),
            CustomSubmit('submit', 'Sign Up')
        )


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"autofocus": True})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('username'),
            Field('password'),
            CustomSubmit('login', 'Login')
        )


class EmployerOnboardingForm(forms.ModelForm):
    class Meta:
        model = EmployerProfile
        fields = ['company_name', 'thumbnail',
                  'company_website', 'company_description']
        widgets = {
            'thumbnail': ImagePreviewWidget()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('company_name'),
            Field('thumbnail'),
            Field('company_website'),
            Field('company_description'),

            CustomSubmit('submit', 'Complete Profile')
        )


class EmployerInformationForm(forms.ModelForm):
    class Meta:
        model = EmployerProfile
        fields = ['company_name', 'thumbnail',
                  'company_website', 'company_description']
        widgets = {
            'thumbnail': ImagePreviewWidget()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('company_name'),
            Field('thumbnail'),
            Field('company_website'),
            Field('company_description'),

            CustomSubmit('submit', 'Save')
        )


class JobSeekerOnboardingForm(forms.ModelForm):
    class Meta:
        model = JobSeekerProfile
        fields = ['resume', 'skills', 'education', 'profile']

        widgets = {
            'skills': autocomplete.ModelSelect2Multiple(url='skills-autocomplete'),
            'profile': ImagePreviewWidget()

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('profile'),
            Field('resume'),
            Field('skills'),
            Field('education'),
            CustomSubmit('submit', 'Complete Profile')
        )


class JobSeekerInformationForm(forms.ModelForm):
    class Meta:
        model = JobSeekerProfile
        fields = ['resume', 'skills', 'education', 'profile']
        widgets = {
            'skills': autocomplete.ModelSelect2Multiple(url='skills-autocomplete'),
            'profile': ImagePreviewWidget()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('profile'),
            Field('resume'),
            Field('skills'),
            Field('education'),
            CustomSubmit('submit', 'Save')
        )


class CustomPasswordResetForm(PasswordResetForm):

    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(
            attrs={'class': 'w-full border p-2 rounded-md'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('email'),
            CustomSubmit('submit', 'Reset Password')
        )
