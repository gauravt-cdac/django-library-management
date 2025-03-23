# Import the Django admin module and URL functions
from django.contrib import admin
from django.urls import path, include

# Define the URL patterns for the project
urlpatterns = [
    # URL for the Django admin panel.
    # This allows access to the built-in Django admin interface.
    path('admin/', admin.site.urls),

    # Include URLs from the "books" app.
    # The empty string ('') means these URLs will be the main URLs for the site.
    path('', include('books.urls')),
]
