from django.urls import path
from customers.views import LoginAPIView, UserSignupAPIView, LogoutAPIView,PlanListAPIView,SimulatePaymentAPIView, CompanyAndTenantAdminSignupAPIView, UserLimitAPIView

urlpatterns = [
    path('signup/', CompanyAndTenantAdminSignupAPIView.as_view(), name='company_signup'),
    path('user-signup/', UserSignupAPIView.as_view(), name='user_signup'),
    path('login/', LoginAPIView.as_view(), name='company_login'),
    path('logout/', LogoutAPIView.as_view(), name='company_logout'),
    path('plans/', PlanListAPIView.as_view(), name='company_logout'),
    path('simulate-payment/', SimulatePaymentAPIView.as_view(), name='simulate_payment'),
    path('user-limit/', UserLimitAPIView.as_view(), name='user_limit'),
]



