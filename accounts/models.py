from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from jsite.settings import MEDIA_ROOT


class UserProfile(models.Model):
    USER_TYPES = [
        ('employer', 'Employer'),
        ('job_seeker', 'Job Seeker'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPES)
    completed_onboarding = models.BooleanField(
        default=False)  # Track onboarding status

    def __str__(self):
        return f"{self.user.username} - {self.user_type}"

    def get_absolute_url(self):
        if self.user_type == "employer":
            return self.user.employerprofile.get_absolute_url()
        else:
            return self.user.jobseekerprofile.get_absolute_url()


class EmployerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    company_website = models.URLField(blank=True, null=True)
    company_description = models.TextField()
    thumbnail = models.ImageField(
        # Add thumbnail field
        upload_to="thumbnails/", blank=True, null=True)

    def __str__(self):
        return self.company_name

    @property
    def s_type(self):
        return "Employer"

    @property
    def s_description(self):
        return self.company_description[:100]

    def get_absolute_url(self):
        return reverse("company_detail", kwargs={"pk": self.pk})


class JobSeekerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    resume = models.FileField(upload_to="resumes/")
    skills = models.ManyToManyField(
        "board.Skill", blank=True, help_text="Skills you posess"
    )
    education = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.username

    @property
    def s_type(self):
        return "Job Seeker"

    @property
    def s_description(self):
        return self.education

    def get_absolute_url(self):
        return reverse("job_seeker_detail", kwargs={"pk": self.pk})
