# Generated by Django 5.1.6 on 2025-02-05 20:06

import address.models
import django.db.models.deletion
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("address", "0003_auto_20200830_1851"),
        ("board", "0003_remove_joblisting_location_joblisting_location_city_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="joblisting",
            name="location_city",
        ),
        migrations.RemoveField(
            model_name="joblisting",
            name="location_country",
        ),
        migrations.RemoveField(
            model_name="joblisting",
            name="location_state",
        ),
        migrations.AddField(
            model_name="joblisting",
            name="location",
            field=address.models.AddressField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="address.address",
            ),
        ),
    ]
