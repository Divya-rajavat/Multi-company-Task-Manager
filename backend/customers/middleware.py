from django.utils.deprecation import MiddlewareMixin
from django_tenants.utils import schema_context
from customers.models import Client
from django.db import connection

class TenantHeaderMiddleware(MiddlewareMixin):
    def process_request(self, request):
        schema = request.headers.get('X-Tenant-Schema')
        if not schema:
            return  

        try:
            tenant = Client.objects.get(schema_name=schema)
            request.tenant = tenant  
            connection.set_tenant(request.tenant)
        except Client.DoesNotExist:
            return  
