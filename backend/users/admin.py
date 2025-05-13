from django.contrib import admin
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import connection 

User = get_user_model()

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role')

    def save_model(self, request, obj, form, change):
        if not obj.pk:  
            tenant = connection.tenant
            user_count = User.objects.count()

            if user_count >= tenant.user_limit:
                raise ValidationError("User limit reached for this tenant.")

        super().save_model(request, obj, form, change)
