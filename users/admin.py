from django.contrib import admin
from .models import User

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'role', 'branch', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('role', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'name', 'branch')
    ordering = ('email',)

    def save_model(self, request, obj, form, change):
        # Hash password if it is changed or new
        if obj.password and not obj.password.startswith('pbkdf2_sha256$'):
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)
