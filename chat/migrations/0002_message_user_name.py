# Generated by Django 4.2.7 on 2023-12-03 18:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chat", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="message",
            name="user_name",
            field=models.TextField(default=None),
        ),
    ]
