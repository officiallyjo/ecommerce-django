from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account  # Importing the custom user model

# Register your models here.

# Define a custom admin class for managing the Account model in the Django admin interface
class AccountAdmin(UserAdmin):
    # Fields to display in the admin list view (the table of users)
    list_display = (
        'email',  # Display the user's email address
        'first_name',  # Display the user's first name
        'last_name',  # Display the user's last name
        'username',  # Display the user's username
        'last_login',  # Display the last time the user logged in
        'date_joined',  # Display the date the user joined
        'is_active'  # Display whether the user's account is active
    )
    
    # Fields that should be clickable links in the admin list view, leading to the user's detail page
    list_display_links = (
        'email',  # Make the email address a clickable link
        'first_name',  # Make the first name a clickable link
        'last_name'  # Make the last name a clickable link
    )
    
    # Fields that should be read-only in the admin detail/edit view
    readonly_fields = (
        'last_login',  # Make the last login time read-only
        'date_joined'  # Make the date joined read-only
    )
    
    # Default ordering of the records in the admin list view
    ordering = ('-date_joined',)  # Order by date joined in descending order (most recent first)
    
    # Fields below are required by UserAdmin but are not being customized in this example

    # Used for horizontal filter widgets, typically for many-to-many relationships; not used here
    filter_horizontal = ()
    
    # Filters that will appear in the right sidebar of the admin list view; not used here
    list_filter = ()
    
    # Layout configuration for the admin detail/edit view; not used here
    fieldsets = ()

# Register the Account model with the custom AccountAdmin class
# This connects the Account model to the Django admin interface using the specified customizations
admin.site.register(Account, AccountAdmin)
