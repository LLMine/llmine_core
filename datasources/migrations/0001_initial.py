# Generated by Django 4.2.2 on 2023-08-20 10:22

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Datasource",
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
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("datasource_name", models.CharField(max_length=255, unique=True)),
                (
                    "datasource_type_name",
                    models.CharField(
                        choices=[("standard", "standard")], max_length=255
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
