from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated,BasePermission
from django.contrib.auth import get_user_model, authenticate
from django.db import transaction
from rest_framework.authtoken.models import Token
from .models import Client, Domain, Plan, Payment
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate
from django_tenants.utils import schema_context
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from datetime import date, timedelta
import random

User = get_user_model()

@method_decorator(csrf_exempt, name='dispatch')
class CompanyAndTenantAdminSignupAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        company_name = request.data.get('company_name')
        tenant_admin_username = request.data.get('tenant_admin_username')
        tenant_admin_email = request.data.get('tenant_admin_email')
        tenant_admin_password = request.data.get('tenant_admin_password')
        plan_name = request.data.get('plan')


        user_limit_map = {
            "basic": 5,
            "premium": 15,
            "enterprise": 100
        }

        user_limit = user_limit_map.get(plan_name.lower(), 5)

        required_fields = [company_name, tenant_admin_username, tenant_admin_email, tenant_admin_password, plan_name]
        if not all(required_fields):
            return Response({"detail": "All fields are required, including plan."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            plan = Plan.objects.get(name=plan_name)
        except Plan.DoesNotExist:
            return Response({"detail": "Invalid plan selected."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                schema_name = company_name.lower()
                if Client.objects.filter(schema_name=schema_name).exists():
                    return Response({"detail": "Tenant with this company name already exists."}, status=400)

                today = date.today()
                trial_end_date = today + timedelta(days=plan.trial_days)
                paid_until_date = today + timedelta(days=plan.duration_days)

                tenant = Client.objects.create(
                    schema_name=schema_name,
                    name=company_name,
                    paid_until=paid_until_date,
                    on_trial=True,
                    plan=plan,
                    user_limit=user_limit
                )

                Domain.objects.create(
                    domain = f"{schema_name}.localhost",
                    tenant=tenant,
                    is_primary=True
                )

            with schema_context(schema_name):
                with transaction.atomic():
                    if User.objects.filter(username=tenant_admin_username).exists():
                        return Response({"detail": "Username already exists in this tenant."}, status=400)

                    tenant_admin = User.objects.create_user(
                        username=tenant_admin_username,
                        email=tenant_admin_email,
                        password=tenant_admin_password,
                        is_staff=True,
                        is_superuser=True
                    )

            return Response({
                "detail": f"Tenant '{company_name}' with plan '{plan_name}' and admin '{tenant_admin_username}' created successfully.",
                "tenant": schema_name,
                "admin": tenant_admin_username,
                "plan": plan_name,
                "domain": f"{schema_name}.localhost"
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







class SimulatePaymentAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        company_name = request.data.get('company_name')
        plan_name = request.data.get('plan')
        payment_status = request.data.get('payment_status')  

        if not company_name or not plan_name:
            return Response({"detail": "company_name and plan are required."}, status=status.HTTP_400_BAD_REQUEST)


        if payment_status not in ['success', 'failed']:
            payment_status = 'failed'
            return Response({"detail": "Invalid payment status."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            plan = Plan.objects.get(name__iexact=plan_name)
        except Plan.DoesNotExist:
            return Response({"detail": "Invalid plan selected."}, status=status.HTTP_400_BAD_REQUEST)

        amount = plan.price

        payment = Payment.objects.create(
            company_name=company_name,
            plan=plan.name,
            amount=amount,
            status=payment_status
        )

        return Response({
            "status": payment_status,
            "amount": amount,
            "plan": plan.name,
            "company_name": company_name,
            "payment_id": payment.id
        }, status=status.HTTP_200_OK)








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

        User = get_user_model()

        if is_base_domain:
            schema_name = request.data.get('schema_name')
            if not schema_name:
                return Response({"detail": "Schema name required on base domain."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                with schema_context(schema_name):
                    with transaction.atomic():
                        if User.objects.filter(is_superuser=True).exists():
                            return Response({"detail": "Superuser already exists for this tenant."}, status=400)

                        if User.objects.filter(username=username).exists():
                            return Response({"detail": "Username already exists in this tenant."}, status=400)

                        user = User.objects.create_user(
                            username=username,
                            email=email,
                            password=password,
                            is_staff=True,
                            is_superuser=True
                        )

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
                        user_count = User.objects.count()
                        user_limit = request.tenant.user_limit or 5

                        if user_count >= user_limit:
                            return Response({"detail": "User limit reached for your plan."}, status=400)

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






@method_decorator(csrf_exempt, name='dispatch')
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





class PlanListAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        plans = Plan.objects.all()
        data = [
            {
                "id": plan.id,
                "name": plan.name,
                "price": str(plan.price),
                "duration_days": plan.duration_days,
                "trial_days": plan.trial_days
            }
            for plan in plans
        ]
        return Response(data)








class UserLimitAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        tenant = request.tenant
        user_model = get_user_model()
        current_user_count = user_model.objects.count()

        return Response({
            "user_limit": tenant.user_limit,
            "current_users": current_user_count,
            "remaining": max(tenant.user_limit - current_user_count, 0)
        })