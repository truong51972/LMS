# Generated by Django 5.0.9 on 2024-09-26 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0013_rename_img_list_sub_module_image_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sub_module',
            name='content_html_list',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sub_module',
            name='image_list',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sub_module',
            name='video_url',
            field=models.TextField(blank=True, null=True),
        ),
    ]
