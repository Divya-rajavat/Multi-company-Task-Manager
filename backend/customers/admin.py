from django.contrib import admin
from customers.models import Client,Domain,Plan

# Register your models here.
admin.site.register(Client)
admin.site.register(Domain)
admin.site.register(Plan)