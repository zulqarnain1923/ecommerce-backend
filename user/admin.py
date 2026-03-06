from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from user.models import User,Addtocart

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('name','email','password', 'is_staff', 'is_active')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('name','email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

admin.site.register(User, CustomUserAdmin)


@admin.register(Addtocart)
class AddtocartAdmin(admin.ModelAdmin):
    list_display=['id','user','created_at','updated_at']