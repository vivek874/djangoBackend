# Generated by Django 5.1.6 on 2025-06-20 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0026_dailyroutine"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="dailyroutine",
            name="title",
        ),
        migrations.AddField(
            model_name="dailyroutine",
            name="grade",
            field=models.CharField(default=1, max_length=10),
            preserve_default=False,
        ),
    ]
