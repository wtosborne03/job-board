# Generated by Django 5.1.6 on 2025-02-05 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("board", "0004_remove_joblisting_location_city_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="joblisting",
            name="salary",
        ),
        migrations.RemoveField(
            model_name="joblisting",
            name="salary_currency",
        ),
        migrations.AddField(
            model_name="joblisting",
            name="salary_max",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="joblisting",
            name="salary_min",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
