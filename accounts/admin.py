from django.contrib import admin

from .models import User,UserProfile

@admin.register(User)
class AccountsUserAdmin(admin.ModelAdmin):
    list_display = ['id','email' ,'username', 'first_name', 'last_name' ,'phone_number','is_admin','is_superadmin','is_staff','is_active']

@admin.register(UserProfile)
class AccountsUserProfileAdmin(admin.ModelAdmin):
    list_display = ['id','user','country','state','city','created_at','modified_at']