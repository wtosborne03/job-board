import django_tables2 as tables
from .models import Application


class ApplicationTable(tables.Table):
    detail = tables.TemplateColumn(
        template_name='board/components/_application_detail_link.html', verbose_name='Detail', orderable=False)

    class Meta:
        model = Application
        template_name = "table/tailwind_table.html"
        fields = ("job_listing.title", "status", "submitted_date")


class JobListingApplicationTable(tables.Table):
    applicant = tables.Column(
        accessor='applicant.user.username', verbose_name='Applicant')
    status = tables.Column(accessor='get_status_display',
                           verbose_name='Status')
    detail = tables.TemplateColumn(
        template_name='board/components/_application_detail_link.html', verbose_name='Detail', orderable=False)

    class Meta:
        model = Application
        fields = ('applicant', 'status')
        template_name = "table/tailwind_table.html"
