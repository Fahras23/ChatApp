# Generated by Django 4.2.7 on 2024-01-17 10:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chat", "0006_remove_message_timestamp_message_date_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="room",
            name="user",
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
