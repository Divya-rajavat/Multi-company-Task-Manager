from django.urls import path
from .views import UserListAPIView, ThemeSettingsView

urlpatterns = [
    path('users/', UserListAPIView.as_view(), name='user-list'),
    path('theme/', ThemeSettingsView.as_view(), name='company_theme'),
]
