# Generated by Django 4.2.2 on 2023-08-20 19:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0005_extracterprompt_extracter_chain"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProcessedData",
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
                ("prompt_result", models.TextField()),
                (
                    "chain",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.extracterchain",
                    ),
                ),
                (
                    "content_pool",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.contentpool",
                    ),
                ),
                (
                    "injested_text_content",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.injestedtextcontent",
                    ),
                ),
                (
                    "prompt",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.extracterprompt",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]