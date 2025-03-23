from django.contrib import admin
from .models import Book, AdminUser

# Register your models here.
admin.site.register(Book)        # Register the Book model to appear in the Django admin interface.
admin.site.register(AdminUser)   # Register the custom AdminUser model for admin management.
