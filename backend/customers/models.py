from django_tenants.models import TenantMixin, DomainMixin
from django.db import models



class Plan(models.Model):
    name = models.CharField(max_length=50, unique=True)  
    trial_days = models.PositiveIntegerField(default=7)  
    duration_days = models.PositiveIntegerField(default=30)  
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Client(TenantMixin):
    name = models.CharField(max_length=100)
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True, blank=True)
    user_limit = models.PositiveIntegerField(default=5)  
    paid_until = models.DateField()
    on_trial = models.BooleanField(default=True)

    auto_create_schema = True

    def __str__(self):
        return self.name

class Domain(DomainMixin):
    pass

