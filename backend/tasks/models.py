from django.db import models
from django.conf import settings

class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='created_tasks', on_delete=models.CASCADE, null=True, blank=True
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='assigned_tasks', on_delete=models.CASCADE, null=True, blank=True
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title