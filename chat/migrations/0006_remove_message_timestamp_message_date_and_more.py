# Generated by Django 4.2.7 on 2023-12-03 18:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chat", "0005_remove_message_user_name"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="message",
            name="timestamp",
        ),
        migrations.AddField(
            model_name="message",
            name="date",
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name="message",
            name="content",
            field=models.CharField(max_length=1000000),
        ),
        migrations.AlterField(
            model_name="message",
            name="room",
            field=models.CharField(max_length=1000000),
        ),
        migrations.AlterField(
            model_name="message",
            name="user",
            field=models.CharField(max_length=1000000),
        ),
    ]