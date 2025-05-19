from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated,BasePermission
from django.contrib.auth import get_user_model, authenticate
from django.db import transaction
from rest_framework.authtoken.models import Token
from .models import Client, Domain
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate
from django_tenants.utils import schema_context
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication


User = get_user_model()

@method_decorator(csrf_exempt, name='dispatch')
class CompanySignupAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        current_tenant = getattr(request, 'tenant', None)

        if not current_tenant or current_tenant != 'public':
            return Response(
                {"detail": "Tenant can only be created from the public schema."},
                status=status.HTTP_400_BAD_REQUEST
            )

        company_name = request.data.get('company_name')
        username = request.data.get('username')
        password = request.data.get('password')

        if not company_name or not username or not password:
            return Response({"detail": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if not user or not user.is_superuser:
            return Response({"detail": "Invalid superuser credentials."}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            with transaction.atomic():
                tenant = Client(
                    schema_name=company_name.lower(),
                    name=company_name,
                    paid_until='2025-12-31',
                    on_trial=True
                )
                tenant.save()

                domain = Domain()
                domain.domain = f'{company_name.lower()}.localhost'
                domain.tenant = tenant
                domain.is_primary = True
                domain.save()

            return Response({
                "detail": f"Tenant '{company_name}' created successfully.",
                "tenant": tenant.schema_name,
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






class RegisterTenantAdminAPIView(APIView):
    permission_classes = []

    def post(self, request):
        host = request.get_host().split(':')[0]  
        schema_name = None

        if host == "localhost":
            schema_name = request.data.get('schema_name')  
            if not schema_name:
                return Response({"detail": "Schema name required on base domain."}, status=400)
        else:
            subdomain = host.split('.')[0]
            schema_name = subdomain

        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not username or not email or not password:
            return Response({"detail": "Username, email, and password are required."}, status=400)

        try:
            with schema_context(schema_name):
                with transaction.atomic():
                    if User.objects.filter(username=username).exists():
                        return Response({"detail": "Username already exists in this tenant."}, status=400)

                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.is_staff = True
                    user.is_superuser = True
                    user.save()

            return Response({"detail": f"Admin '{username}' created for tenant '{schema_name}'."}, status=201)

        except Exception as e:
            return Response({"detail": str(e)}, status=500)








@method_decorator(csrf_exempt, name='dispatch')
class UserSignupAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        host = request.get_host().split(':')[0]
        is_base_domain = host == "localhost"

        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not username or not email or not password:
            return Response({"detail": "Username, email, and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        if is_base_domain:
            schema_name = request.data.get('schema_name')
            if not schema_name:
                return Response({"detail": "Schema name required on base domain."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                with schema_context(schema_name):
                    with transaction.atomic():
                        User = get_user_model()
                        if User.objects.filter(username=username).exists():
                            return Response({"detail": "Username already exists in this tenant."}, status=400)

                        user = User.objects.create_user(username=username, email=email, password=password)
                        user.is_staff = True
                        user.is_superuser = True
                        user.save()

                        token, _ = Token.objects.get_or_create(user=user)

                return Response({
                    "detail": f"Admin '{username}' created for tenant '{schema_name}'.",
                    "token": token.key
                }, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({"detail": str(e)}, status=500)

        else:
            try:
                with schema_context(request.tenant.schema_name):
                    with transaction.atomic():
                        User = get_user_model()
                        if User.objects.filter(username=username).exists():
                            return Response({"detail": "Username already exists."}, status=400)

                        user = User.objects.create_user(username=username, email=email, password=password)
                        token, _ = Token.objects.get_or_create(user=user)

                return Response({
                    "detail": "User signed up successfully.",
                    "token": token.key,
                    "username": user.username,
                    "tenant": request.tenant.schema_name
                }, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({"detail": str(e)}, status=500)








@method_decorator(csrf_exempt, name='dispatch')
class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        schema_name = request.data.get('schema_name')  

        try:
            current_schema = request.tenant.schema_name
        except AttributeError:
            current_schema = 'public'

        if current_schema == 'public':
            if not schema_name:
                return Response(
                    {"detail": "Company name is required."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            try:
                with schema_context(schema_name):
                    user = authenticate(username=username, password=password)
                    if user is None:
                        return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

                    token, _ = Token.objects.get_or_create(user=user)

                    return Response({
                        "detail": "Login successful.",
                        "token": token.key,
                        "tenant": schema_name,
                        "username": user.username
                    })
            except Exception as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        else:
            user = authenticate(username=username, password=password)
            if user is None:
                return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

            token, _ = Token.objects.get_or_create(user=user)

            return Response({
                "detail": "Login successful.",
                "token": token.key,
                "tenant": current_schema,
                "username": user.username
            })







class LogoutAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        schema_name = request.data.get('schema_name')

        if schema_name and connection.schema_name == 'public':
            try:
                with schema_context(schema_name):
                    request.user.auth_token.delete()
            except Exception as e:
                return Response({"detail": "Logout failed."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            request.user.auth_token.delete()

        return Response({"detail": "Logout successful."}, status=status.HTTP_200_OK)


