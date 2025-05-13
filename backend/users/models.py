from django.contrib.auth.models import AbstractUser
from guardian.models import UserObjectPermission
from django.db import models

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

