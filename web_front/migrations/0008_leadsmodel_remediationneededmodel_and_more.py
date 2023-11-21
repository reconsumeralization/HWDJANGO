# Generated by Django 4.2.6 on 2023-11-21 20:44

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):
    dependencies = [
        ("web_front", "0007_customermodel_created_by_customermodel_updated_by"),
    ]

    operations = [
        migrations.CreateModel(
            name="LeadsModel",
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
                ("last_name", models.CharField(max_length=30)),
                ("first_name", models.CharField(max_length=30)),
                ("email", models.EmailField(blank=True, max_length=254)),
                (
                    "phone_number",
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True, max_length=128, null=True, region="US"
                    ),
                ),
                (
                    "alt_phone_number",
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True, max_length=128, null=True, region="US"
                    ),
                ),
                ("created_by", models.CharField(blank=True, max_length=30)),
                ("updated_by", models.CharField(blank=True, max_length=30)),
                ("lead_source", models.CharField(blank=True, max_length=30)),
                ("subscribed", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="RemediationNeededModel",
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
                ("last_name", models.CharField(max_length=30)),
                ("first_name", models.CharField(max_length=30)),
                ("email", models.EmailField(blank=True, max_length=254)),
                (
                    "phone_number",
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True, max_length=128, null=True, region="US"
                    ),
                ),
                (
                    "alt_phone_number",
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True, max_length=128, null=True, region="US"
                    ),
                ),
                ("created_by", models.CharField(blank=True, max_length=30)),
                ("updated_by", models.CharField(blank=True, max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name="customermodel",
            name="subscribed",
            field=models.BooleanField(default=False),
        ),
    ]
