# Generated by Django 4.2.7 on 2023-12-03 18:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chat", "0002_message_user_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="message",
            name="user_name",
            field=models.TextField(default=None, null=True),
        ),
    ]