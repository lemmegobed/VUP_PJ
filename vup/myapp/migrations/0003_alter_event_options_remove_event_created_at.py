# Generated by Django 5.1.3 on 2024-12-13 20:13

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0002_delete_notification"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="event",
            options={},
        ),
        migrations.RemoveField(
            model_name="event",
            name="created_at",
        ),
    ]