from django.urls import path
from . import views  # Import views module directly for better structure

urlpatterns = [
    # 🔹 Admin Authentication Views
    path("signup/", views.admin_signup, name="admin_signup"),  # Admin signup: Creates a new admin account
    path("login/", views.admin_login, name="admin_login"),      # Admin login: Authenticates an admin user
    path("logout/", views.logout_view, name="logout"),          # Logout: Logs out the current admin user

    # 🔹 Admin Book Management Views (Django Template-Based)
    path("books/", views.admin_books, name="admin_books"),      # List all books for admin management
    path("books/add/", views.add_book, name="add_book"),          # Add a new book record
    path("books/update/<int:book_id>/", views.update_book, name="update_book"),  # Update details of a specific book
    path("books/delete/<int:book_id>/", views.delete_book, name="delete_book"),  # Delete a specific book

    # 🔹 Student View (Template-Based)
    path("books/view/", views.student_book_list, name="student_books"),  # Student view: Lists all books for public access

    # 🔹 REST API Endpoints (Django REST Framework)
    path("api/register/", views.RegisterAdminView.as_view(), name="register"),  # API endpoint to register admin users
    path("api/login/", views.LoginAdminView.as_view(), name="login"),           # API endpoint for admin login and JWT token retrieval
    path("api/books/", views.BookListCreateView.as_view(), name="book-list"),     # API endpoint to list all books and create new ones
    path("api/books/<int:pk>/", views.BookRetrieveUpdateDestroyView.as_view(), name="book-detail"),  # API endpoint to retrieve, update, or delete a specific book
]
