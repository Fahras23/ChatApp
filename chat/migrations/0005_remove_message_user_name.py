# Generated by Django 4.2.7 on 2023-12-03 18:10

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("chat", "0004_alter_message_user_name"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="message",
            name="user_name",
        ),
    ]
