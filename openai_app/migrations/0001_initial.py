# Generated by Django 4.2.2 on 2023-08-21 15:40

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="OpenAICallLog",
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
                ("usage_type", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "used_in_module",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("prompt_token", models.IntegerField(blank=True, null=True)),
                ("total_token", models.IntegerField(blank=True, null=True)),
                ("openai_resp", models.TextField(blank=True, null=True)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]