# Generated by Django 4.2.2 on 2023-08-21 15:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0007_alter_extracterchain_content_pool"),
    ]

    operations = [
        migrations.AddField(
            model_name="injestedtextcontent",
            name="process_completed_successfully",
            field=models.BooleanField(blank=True, null=True),
        ),
    ]