from django.utils.deprecation import MiddlewareMixin
from django_tenants.utils import schema_context
from customers.models import Client
from django.db import connection
from django_tenants.utils import get_public_schema_name

class TenantHeaderMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if 'create-tenant' in request.path:
            request.tenant = 'public'
            return
        schema = request.headers.get('X-Tenant-Schema')


        try:
            tenant = Client.objects.get(schema_name=schema)
            request.tenant = tenant
            connection.set_tenant(tenant)
        except Client.DoesNotExist:
            connection.set_schema_to_public()

