from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework.authtoken.models import Token
from .models import Client, Domain
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate
from django_tenants.utils import schema_context


User = get_user_model()

@method_decorator(csrf_exempt, name='dispatch')
class CompanySignupAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        company_name = request.data.get('company_name')
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not company_name or not username or not email or not password:
            return Response({"detail": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

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

                with schema_context(tenant.schema_name):
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.is_staff = True
                    user.save()

                    token, _ = Token.objects.get_or_create(user=user)

                return Response({
                    "detail": f"Company '{company_name}' and admin user created successfully.",
                    "tenant": tenant.schema_name,
                    "admin_user": username,
                    "token": token.key
                }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch')
class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        print("🔍 Current schema:", request.tenant.schema_name)

        User = get_user_model()
        user = User.objects.filter(username=username).first()

        if user:
            print("User exists:", user.username)
            print("Password correct?", user.check_password(password))
        else:
            print("No such user found in this schema.")


        user = authenticate(username=username, password=password)
        if user is None:
            return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            "detail": "Login successful.",
            "token": token.key,
            "tenant": request.tenant.schema_name,
            "username": user.username
        }, status=status.HTTP_200_OK)


