from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserImage, UserMessages
from .forms import AdminUserCreationForm, AdminUserChangeForm


class CustomUserAdmin(UserAdmin):
    add_form = AdminUserCreationForm
    form = AdminUserChangeForm
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active', 'is_instructor')
    list_filter = ('email', 'is_staff', 'is_active', 'is_instructor')
    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name', 'last_name', 'birthday', 'image_profile', 'phone_number',
                           'addressLine1', 'addressLine2', 'city', 'bio', 'link1', 'link2', 'link3', 'tuition')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_instructor')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )

    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserImage)

