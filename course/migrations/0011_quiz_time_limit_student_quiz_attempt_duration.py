# Generated by Django 5.0.9 on 2024-10-15 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0010_alter_student_quiz_attempt_proctoring_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='time_limit',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='student_quiz_attempt',
            name='duration',
            field=models.IntegerField(null=True),
        ),
    ]
