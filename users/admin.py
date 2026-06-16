from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline]
    list_display = ['email', 'username', 'role', 'is_active']
    list_filter = ['role', 'is_active']
    search_fields = ['email', 'username']
    ordering = ['-date_joined']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Rol', {'fields': ('role',)}),
    )

    class Media:
        css = {'all': ('admin/css/custom_admin.css',)}


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'birthdate', 'created_at']
    search_fields = ['user__email']

    class Media:
        css = {'all': ('admin/css/custom_admin.css',)}


admin.site.site_header = "Northdemy Admin"
admin.site.site_title = "Northdemy"
admin.site.index_title = "Panel de administración"