from django.contrib.auth.models import AbstractUser
from guardian.models import UserObjectPermission
from django.db import models
from customers.models import Client

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('employee', 'Employee'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def delete(self, *args, **kwargs):
        UserObjectPermission.objects.filter(user=self).delete()
        super().delete(*args, **kwargs)

class Theme(models.Model):
    theme_name = models.CharField(max_length=35, default="theme")
    primary_color = models.CharField(max_length=7, default="#007bff")
    secondary_color = models.CharField(max_length=7, default="#6c757d")
    background_color = models.CharField(max_length=7, default="#ffffff")
    font_family = models.CharField(max_length=100, default="Arial, sans-serif")

    def __str__(self):
        return self.theme_name