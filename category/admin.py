from django.contrib import admin
from .models import Category  # Importing the category model from the current directory

# Register your models here.

# Define a custom admin class for managing the category model in the Django admin interface
class CategoryAdmin(admin.ModelAdmin):
    # Automatically populate the slug field based on the category_name field
    prepopulated_fields = {'slug': ('category_name',)}
    
    # Fields to display in the admin list view (the table of categories)
    list_display = (
        'category_name',  # Display the name of the category
        'slug'  # Display the slug of the category
    )
    
# Register the category model with the custom CategoryAdmin class
# This connects the category model to the Django admin interface using the specified customizations
admin.site.register(Category, CategoryAdmin)
