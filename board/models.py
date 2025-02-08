from django.db import models
from accounts.models import EmployerProfile, UserProfile
from address.models import AddressField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from prose.fields import RichTextField


class EmploymentType(models.TextChoices):
    FULL_TIME = "Full-time", _("Full-time")
    PART_TIME = "Part-time", _("Part-time")
    CONTRACT = "Contract", _("Contract")
    INTERNSHIP = "Internship", _("Internship")
    FREELANCE = "Freelance", _("Freelance")


class ExperienceLevel(models.TextChoices):
    ENTRY = "Entry-level", _("Entry-level")
    MID = "Mid-level", _("Mid-level")
    SENIOR = "Senior-level", _("Senior-level")
    EXECUTIVE = "Executive", _("Executive")


class RemoteType(models.TextChoices):
    ONSITE = "On-site", _("On-site")
    HYBRID = "Hybrid", _("Hybrid")
    REMOTE = "Remote", _("Remote")


class JobStatus(models.TextChoices):
    OPEN = "Open", _("Open")
    CLOSED = "Closed", _("Closed")
    DRAFT = "Draft", _("Draft")
    PENDING = "Pending Approval", _("Pending Approval")


class JobCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Benefit(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class JobListing(models.Model):
    employer = models.ForeignKey(
        EmployerProfile, on_delete=models.CASCADE, related_name='job_listings')
    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        JobCategory, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField()
    location = AddressField(related_name='+', blank=True, null=True)
    salary_min = models.IntegerField(
        null=True, blank=True, help_text='Minimum salary in USD')
    salary_max = models.IntegerField(
        null=True, blank=True, help_text='Maximum salary in USD')
    employment_type = models.CharField(
        max_length=20, choices=EmploymentType.choices, default=EmploymentType.FULL_TIME
    )
    experience_level = models.CharField(
        max_length=20, choices=ExperienceLevel.choices, default=ExperienceLevel.ENTRY
    )
    education_required = models.CharField(
        max_length=255, null=True, blank=True, help_text="E.g., Bachelor's degree, High school diploma"
    )
    skills_required = models.ManyToManyField(
        "Skill", blank=True, help_text="Required skills for the job"
    )
    benefits = models.ManyToManyField(
        "Benefit", blank=True, help_text="Benefits offered by the employer"
    )

    application_url = models.URLField(
        max_length=500, null=True, blank=True, help_text="External application link"
    )
    application_instructions = models.TextField(
        null=True, blank=True, help_text="Instructions for applying (e.g., cover letter requirements)"
    )
    hiring_process = models.TextField(
        null=True, blank=True, help_text="Description of interview process"
    )

    is_remote = models.BooleanField(default=False)
    remote_type = models.CharField(
        max_length=10, choices=RemoteType.choices, default=RemoteType.ONSITE
    )

    status = models.CharField(
        max_length=20, choices=JobStatus.choices, default=JobStatus.OPEN
    )
    views_count = models.PositiveIntegerField(default=0)
    posted_date = models.DateTimeField(auto_now_add=True)
    application_deadline = models.DateTimeField()

    def __str__(self):
        return self.title

    @property
    def s_type(self):
        return "Job Listing"

    @property
    def s_description(self):
        return self.description[:100]

    def get_absolute_url(self):
        return reverse("job_detail", kwargs={"pk": self.pk})


class Message(models.Model):
    sender = models.ForeignKey(
        UserProfile, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(
        UserProfile, related_name='received_messages', on_delete=models.CASCADE)
    content = RichTextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    parent = models.ForeignKey(
        'self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    def __str__(self):
        return f"Message from {self.sender} to {self.recipient} at {self.timestamp}"


class ApplicationStatus(models.TextChoices):
    SUBMITTED = "Submitted", _("Submitted")
    UNDER_REVIEW = "Under Review", _("Under Review")
    INTERVIEW = "Interview", _("Interview")
    OFFER = "Offer", _("Offer")
    REJECTED = "Rejected", _("Rejected")


class Application(models.Model):
    job_listing = models.ForeignKey(
        JobListing, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='applications')
    cover_letter = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=ApplicationStatus.choices, default=ApplicationStatus.SUBMITTED)
    submitted_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Application by {self.applicant} for {self.job_listing}"

    def get_absolute_url(self):
        return reverse("application_detail", kwargs={"pk": self.pk})
