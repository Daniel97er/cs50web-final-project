# Generated by Django 4.2.3 on 2023-08-15 12:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("crm_system", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="task_date",
            field=models.DateField(blank=True, null=True),
        ),
    ]