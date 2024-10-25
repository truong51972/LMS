from django.db import models

class Subject(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

import mimetypes

class Material(models.Model):
    MATERIAL_TYPE_CHOICES = [
        ('assignments', 'Assignments'),
        ('labs', 'Labs'),
        ('lectures', 'Lectures'),
    ]
    
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='materials')
    material_type = models.CharField(max_length=20, choices=MATERIAL_TYPE_CHOICES)
    file = models.FileField(upload_to='materials/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject.name} - {self.get_material_type_display()}"

    def get_file_type(self):
        """Returns the MIME type of the file."""
        if self.file:
            mime_type, _ = mimetypes.guess_type(self.file.name)
            return mime_type or 'Unknown'
        return 'No file'

