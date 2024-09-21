from django.db import models
from django.core.cache import cache
from django.utils.timezone import now

from user.models import User

from unidecode import unidecode

import os


class Course(models.Model):
    course_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True, max_length=500)
    image = models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def delete(self, *args, **kwargs):
        try:
            self.image.delete()
        except PermissionError:
            print('Error!')

        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.image:
            name, ext = os.path.splitext(self.image.name)
            new_filename = f"{unidecode(name)}{ext}"
            self.image.name = new_filename

        super().save(*args, **kwargs)

    def __str__(self):
        return self.course_name


class Enrolled_course(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course')