# Generated by Django 4.2.2 on 2023-08-20 12:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0004_remove_extracterprompt_content_pool_extracterchain"),
    ]

    operations = [
        migrations.AddField(
            model_name="extracterprompt",
            name="extracter_chain",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="core.extracterchain",
            ),
            preserve_default=False,
        ),
    ]
