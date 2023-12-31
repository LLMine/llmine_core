# Generated by Django 4.2.2 on 2023-08-21 15:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0006_processeddata"),
    ]

    operations = [
        migrations.AlterField(
            model_name="extracterchain",
            name="content_pool",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="extracter_chains",
                to="core.contentpool",
            ),
        ),
    ]
