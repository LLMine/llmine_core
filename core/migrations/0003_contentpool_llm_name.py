# Generated by Django 4.2.2 on 2023-08-20 12:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_remove_injestedtextcontent_datasource_type_name_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="contentpool",
            name="llm_name",
            field=models.CharField(
                choices=[
                    ("gpt-3.5-turbo", "gpt-3.5-turbo"),
                    ("gpt-3.5-turbo-16k", "gpt-3.5-turbo-16k"),
                    ("gpt-4", "gpt-4"),
                ],
                default="gpt-3.5-turbo-16k",
                max_length=255,
            ),
            preserve_default=False,
        ),
    ]