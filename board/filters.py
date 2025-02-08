import django_filters
from .models import JobListing, EmploymentType
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from jsite.custom_form import CustomSubmit


class JobListingFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    location = django_filters.CharFilter(lookup_expr='icontains')
    employment_type = django_filters.ChoiceFilter(
        choices=EmploymentType.choices)

    class Meta:
        model = JobListing
        fields = ['title', 'location', 'employment_type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form.helper = FormHelper()
        self.form.helper.form_method = 'GET'
        self.form.helper.layout = Layout(
            Field('title'),
            Field('location'),
            Field('employment_type'),
            CustomSubmit(
                'submit', 'Filter', css_class='bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded cursor-pointer mt-7')
        )
        self.form.helper.form_class = 'flex flex-row items-center bg-blue-500'
