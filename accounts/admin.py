from django.contrib import admin

from .models import User

@admin.register(User)
class AccountsUserAdmin(admin.ModelAdmin):
    list_display = ['id','email' ,'username', 'first_name', 'last_name' ,'phone_number']