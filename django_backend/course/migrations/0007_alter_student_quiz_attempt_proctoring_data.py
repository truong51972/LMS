# Generated by Django 5.0.9 on 2024-10-03 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0006_quiz_mark_to_pass'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student_quiz_attempt',
            name='proctoring_data',
            field=models.JSONField(null=True),
        ),
    ]
