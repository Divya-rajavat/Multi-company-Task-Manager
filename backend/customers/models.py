from django_tenants.models import TenantMixin, DomainMixin
from django.db import models

class Client(TenantMixin):
    name = models.CharField(max_length=100)
    user_limit = models.PositiveIntegerField(default=5)  
    paid_until = models.DateField()
    on_trial = models.BooleanField(default=True)

    auto_create_schema = True

    def __str__(self):
        return self.name

class Domain(DomainMixin):
    pass

