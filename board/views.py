from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView
from .forms import JobListingForm, MessageForm
from .models import JobListing, Message
from django.contrib import messages
from .decorators import employer_required
from watson import search as watson
from accounts.models import EmployerProfile, UserProfile, JobSeekerProfile
from django.db.models import F
from dal import autocomplete
from .models import Skill, Benefit, Application
from django_filters.views import FilterView
from .filters import JobListingFilter
from django.views.generic.edit import FormView
from .forms import ReplyForm, ApplicationForm
from django.contrib.auth.mixins import LoginRequiredMixin
import django_tables2 as tables
from .tables import ApplicationTable, JobListingApplicationTable


# Create your views here.
class HomeView(FilterView):
    template_name = "board/home.html"
    context_object_name = 'job_listings'
    model = JobListing
    filterset_class = JobListingFilter

    def get_queryset(self):
        return self.model.objects.all()

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and getattr(request.user, 'userprofile', None) and request.user.userprofile.user_type == 'employer':
            return redirect('employer_home')
        return super().get(request, *args, **kwargs)


@method_decorator([login_required, employer_required], name='dispatch')
class EmployerHomeView(FilterView):
    template_name = "board/employer_home.html"
    context_object_name = 'job_listings'
    model = JobListing
    filterset_class = JobListingFilter

    def get_queryset(self):
        return self.model.objects.filter(employer=self.request.user.employerprofile)


@method_decorator([login_required, employer_required], name='dispatch')
class CreateListingView(CreateView):
    form_class = JobListingForm
    template_name = "board/listing/create_listing.html"
    success_url = '/employer_home/'

    def form_valid(self, form: JobListingForm):
        form.instance.employer = self.request.user.employerprofile
        form.save()
        messages.info(self.request, "Job Listing Created")
        return redirect('employer_home')


class JobDetailView(DetailView):
    model = JobListing
    template_name = 'board/listing/listing.html'
    context_object_name = 'job'

    def get(self, request, *args, **kwargs):
        job = self.get_object()

        # Increment view count safely
        job.views_count = F('views_count') + 1
        job.save(update_fields=['views_count'])

        # Refresh to get updated value
        job.refresh_from_db()

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated and getattr(self.request.user, 'employerprofile', None):
            context['is_owner'] = self.request.user.employerprofile == self.object.employer
            context['applications'] = JobListingApplicationTable(
                self.object.applications.all())

        if self.request.user.is_authenticated and getattr(self.request.user, 'jobseekerprofile', None):
            context['is_job_seeker'] = True
        return context


class CompanyDetailView(DetailView):
    model = EmployerProfile
    template_name = 'board/companies/company_listing.html'
    context_object_name = 'company'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class JobSeekerDetailView(DetailView):
    model = JobSeekerProfile
    template_name = 'board/job_seekers/job_seeker_listing.html'
    context_object_name = 'job_seeker'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@method_decorator([login_required, employer_required], name='dispatch')
class JobEditView(UpdateView):
    model = JobListing
    form_class = JobListingForm
    template_name = 'board/listing/edit_listing.html'

    def get_success_url(self):
        return reverse_lazy('job_detail', kwargs={'pk': self.object.pk})

    def get_queryset(self):
        return self.model.objects.filter(employer=self.request.user.employerprofile)


@method_decorator([login_required, employer_required], name='dispatch')
class JobDeleteView(DeleteView):
    model = JobListing
    template_name = 'board/listing/delete_listing.html'
    success_url = reverse_lazy('employer_home')
    context_object_name = 'job'

    def get_queryset(self):
        return self.model.objects.filter(employer=self.request.user.employerprofile)


def search(request):
    query = request.GET.get('q')
    results = watson.search(query) if query else []

    return render(request, 'board/search_results.html', {'results': results, 'query': query})


class SkillAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = Skill.objects.all()
        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs


class BenefitsAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Benefit.objects.all()
        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs


class UserAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return UserProfile.objects.none()

        qs = UserProfile.objects.all()

        if self.q:
            qs = qs.filter(user__username__icontains=self.q)

        return qs


@login_required
def inbox_view(request):
    received_messages = Message.objects.filter(
        recipient=request.user.userprofile, parent__isnull=True).order_by('-timestamp')
    sent_messages = Message.objects.filter(
        sender=request.user.userprofile, parent__isnull=True).order_by('-timestamp')
    messages = received_messages | sent_messages
    messages = messages.order_by('-timestamp')
    return render(request, 'board/messages/inbox.html', {'m_messages': messages})


class MessageDetailView(LoginRequiredMixin, DetailView, FormView):
    model = Message
    template_name = 'board/messages/message_detail.html'
    context_object_name = 'message'
    form_class = ReplyForm

    def get_success_url(self):
        return reverse_lazy('message_detail', kwargs={'pk': self.get_object().pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def form_valid(self, form):
        print("m_form")
        message = self.get_object()
        form.instance.sender = self.request.user.userprofile
        form.instance.recipient = message.sender if message.sender != self.request.user.userprofile else message.recipient
        form.instance.parent = message
        form.save()
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        message: Message = self.get_object()
        if request.method == 'POST':
            messages.info(request, 'Reply Sent')
        if not message.read and request.user.userprofile == message.recipient:
            message.read = True
            message.save(update_fields=['read'])
        if request.user.userprofile not in [message.sender, message.recipient]:
            return redirect('inbox')
        return super().dispatch(request, *args, **kwargs)


@login_required
def send_message_view(request):
    parent_id = request.POST.get('parent')
    parent = Message.objects.get(pk=parent_id) if parent_id else None
    recipient_id = request.GET.get('recipient')
    recipient = UserProfile.objects.get(
        pk=recipient_id) if recipient_id else None

    if request.method == 'POST':
        form = MessageForm(request.POST, parent=parent)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user.userprofile
            if parent:
                message.recipient = parent.sender if parent.sender != request.user.userprofile else parent.recipient
                message.parent = parent

            message.save()
            messages.info(request, 'Message Sent')
            return redirect('inbox')
    else:
        form = MessageForm(parent=parent, initial={'recipient': recipient})
    return render(request, 'board/messages/send_message.html', {'form': form})


class ApplicationCreateView(LoginRequiredMixin, CreateView):
    model = Application
    form_class = ApplicationForm
    template_name = 'board/applications/application_form.html'

    def form_valid(self, form):
        form.instance.applicant = self.request.user.userprofile
        form.instance.job_listing = JobListing.objects.get(
            pk=self.kwargs['pk'])
        messages.info(self.request, "Application Submitted")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('job_detail', kwargs={'pk': self.object.job_listing.pk})


class ApplicationDetailView(LoginRequiredMixin, DetailView):
    model = Application
    template_name = 'board/applications/application_detail.html'
    context_object_name = 'application'


class MyApplicationsView(LoginRequiredMixin, tables.SingleTableView):
    template_name = 'board/job_seekers/my_applications.html'
    context_object_name = 'applications'
    model = Application
    table_class = ApplicationTable

    def get_queryset(self):
        return self.model.objects.filter(applicant=self.request.user.userprofile)
