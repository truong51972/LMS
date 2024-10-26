# Generated by Django 5.0.9 on 2024-10-18 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0012_remove_student_quiz_attempt_duration'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='using_seb',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='student_quiz_attempt',
            name='duration',
            field=models.IntegerField(default=0),
        ),
    ]