from django.urls import path
from customers.views import CompanySignupAPIView, LoginAPIView, UserSignupAPIView, RegisterTenantAdminAPIView, LogoutAPIView

urlpatterns = [
    path('create-tenant/', CompanySignupAPIView.as_view(), name='company_signup'),
    path('register-admin/', RegisterTenantAdminAPIView.as_view(), name='create-tenant-admin'),
    path('user-signup/', UserSignupAPIView.as_view(), name='user_signup'),
    path('login/', LoginAPIView.as_view(), name='company_login'),
    path('logout/', LogoutAPIView.as_view(), name='company_logout'),
]
