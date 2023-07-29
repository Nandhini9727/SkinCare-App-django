from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account
# Register your models here.

#for making password uneditable we need AccountAdmin class
class AccountAdmin(UserAdmin):
    # to display model object with multiple field instead of a single field
    list_display = ('email','first_name','last_name','username','last_login','date_joined','is_active')
    # to display other fields as links 
    list_display_links = ('email','first_name','last_name') 
    readonly_fields = ('last_login','date_joined') 
    # In danjgo we need to set other parameters to be set for AccountAdmin to work  
    filter_horizontal =()
    list_filter=()
    fieldsets=()
    # model ojects will be displayed in descending order of date_joined since we have mentioned hypen before date_joined
    ordering=('-date_joined',)

# Register the Account and AccountAdmin Model in admin.py to be able to see it in admin panel
admin.site.register(Account, AccountAdmin)