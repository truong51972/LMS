from django.db import models
from role.models import Role

from django.contrib.auth.models import AbstractUser

# class User(models.Model):
#     username = models.CharField(max_length=255, unique=True)
#     password = models.CharField(max_length=255)
#     email = models.EmailField(unique=True)
#     full_name = models.CharField(max_length=255, blank=True, null=True)
#     role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)

#     def __str__(self):
#         return self.username
    
class User(AbstractUser):
    full_name = models.CharField(max_length=255, blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.username