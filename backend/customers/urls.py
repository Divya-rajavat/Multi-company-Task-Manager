from django.urls import path
from customers.views import CompanySignupAPIView,LoginAPIView

urlpatterns = [
    path('signup/', CompanySignupAPIView.as_view(), name='company_signup'),
    path('login/', LoginAPIView.as_view(), name='company_login'),
]
