from django.urls import path
from customers.views import LoginAPIView, UserSignupAPIView, LogoutAPIView,PlanListAPIView, CompanyAndTenantAdminSignupAPIView

urlpatterns = [
    path('signup/', CompanyAndTenantAdminSignupAPIView.as_view(), name='company_signup'),
    path('user-signup/', UserSignupAPIView.as_view(), name='user_signup'),
    path('login/', LoginAPIView.as_view(), name='company_login'),
    path('logout/', LogoutAPIView.as_view(), name='company_logout'),
    path('plans/', PlanListAPIView.as_view(), name='company_logout'),
]
