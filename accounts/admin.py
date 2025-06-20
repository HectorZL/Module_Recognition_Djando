from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, UserProfile, Note

class CustomUserAdmin(UserAdmin):
    """Configuración personalizada para el modelo de usuario en el admin."""
    model = User
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_admin', 'is_superuser')
    list_filter = ('is_admin', 'is_staff', 'is_superuser', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Información personal'), {'fields': ('first_name', 'last_name')}),
        (_('Permisos'), {
            'fields': ('is_active', 'is_staff', 'is_admin', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Fechas importantes'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'is_staff', 'is_admin', 'is_superuser'),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Set default values for new users
        if obj is None:
            form.base_fields['is_staff'].initial = True
            form.base_fields['is_admin'].initial = True
            form.base_fields['is_superuser'].initial = True
        return form


class UserProfileAdmin(admin.ModelAdmin):
    """Configuración para el modelo de perfil de usuario en el admin."""
    list_display = ('user', 'phone', 'created_at')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'phone')
    list_filter = ('created_at',)
    raw_id_fields = ('user',)


class NoteAdmin(admin.ModelAdmin):
    """Configuración para el modelo de notas en el admin."""
    list_display = ('title', 'user', 'created_at', 'updated_at')
    search_fields = ('title', 'content', 'user__email')
    list_filter = ('created_at', 'updated_at')
    raw_id_fields = ('user',)
    date_hierarchy = 'created_at'


# Registrar los modelos en el panel de administración
admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Note, NoteAdmin)
