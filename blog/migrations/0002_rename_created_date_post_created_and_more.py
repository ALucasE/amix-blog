# Generated by Django 4.2 on 2024-08-25 06:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="post",
            old_name="created_date",
            new_name="created",
        ),
        migrations.RenameField(
            model_name="post",
            old_name="updated_date",
            new_name="updated",
        ),
    ]
