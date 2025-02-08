# Generated by Django 5.1.5 on 2025-02-04 19:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userprofile",
            name="company_name",
        ),
        migrations.RemoveField(
            model_name="userprofile",
            name="resume",
        ),
        migrations.AddField(
            model_name="userprofile",
            name="completed_onboarding",
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name="EmployerProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("company_name", models.CharField(max_length=255)),
                ("company_website", models.URLField(blank=True, null=True)),
                ("company_description", models.TextField()),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="JobSeekerProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("resume", models.FileField(upload_to="resumes/")),
                ("skills", models.TextField()),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
