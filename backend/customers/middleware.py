# customers/middleware.py
from django.utils.deprecation import MiddlewareMixin
from django_tenants.utils import schema_context
from customers.models import Client  # adjust if Client is in a different app
from django.db import connection

class TenantHeaderMiddleware(MiddlewareMixin):
    def process_request(self, request):
        schema = request.headers.get('X-Tenant-Schema')
        # schema = schema.split('.')[0]
        if not schema:
            return  # or optionally raise an error / default to 'public'

        try:
            tenant = Client.objects.get(schema_name=schema)
            request.tenant = tenant  # <-- this is enough for TenantMiddleware
            connection.set_tenant(request.tenant)
        except Client.DoesNotExist:
            return  # or raise error
