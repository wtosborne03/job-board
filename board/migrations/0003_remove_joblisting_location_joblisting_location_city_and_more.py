# Generated by Django 5.1.6 on 2025-02-05 19:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("board", "0002_joblisting_salary_currency_alter_joblisting_salary"),
        ("cities_light", "0011_alter_city_country_alter_city_region_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="joblisting",
            name="location",
        ),
        migrations.AddField(
            model_name="joblisting",
            name="location_city",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="cities_light.city",
            ),
        ),
        migrations.AddField(
            model_name="joblisting",
            name="location_country",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="cities_light.country",
            ),
        ),
        migrations.AddField(
            model_name="joblisting",
            name="location_state",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="cities_light.region",
            ),
        ),
    ]
