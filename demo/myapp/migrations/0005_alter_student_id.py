# Generated by Django 5.1.6 on 2025-04-17 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0004_alter_student_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="student",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]
