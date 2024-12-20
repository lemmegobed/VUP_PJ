# Generated by Django 5.1.3 on 2024-12-13 20:32

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0004_remove_event_participants_event_max_participants"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="event",
            options={"ordering": ["-created_at"]},
        ),
        migrations.AddField(
            model_name="event",
            name="created_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
