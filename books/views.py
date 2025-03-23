import re
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Book, AdminUser
from .serializers import BookSerializer, AdminUserSerializer

User = get_user_model()

# 🔹 Utility functions for validation
def is_valid_email(email):
    """
    Check if the email has a valid format.
    Returns a match object if valid, None otherwise.
    """
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email)

def is_valid_password(password):
    """
    Check if the password is strong enough.
    In this case, ensure it is at least 6 characters long.
    """
    return len(password) >= 6

# 🔹 Admin Authentication (API)
class RegisterAdminView(generics.CreateAPIView):
    """
    API view to register a new admin user.
    No authentication is needed for registration.
    """
    queryset = AdminUser.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = [permissions.AllowAny]

class LoginAdminView(generics.GenericAPIView):
    """
    API view to log in an admin user.
    Returns JWT tokens upon successful authentication.
    """
    serializer_class = AdminUserSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=email, password=password)

        if user:
            # Generate refresh and access tokens for the user
            refresh = RefreshToken.for_user(user)
            return Response({
                "user_id": user.id,
                "email": user.email,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            })
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

# 🔹 Book Management API
class BookListCreateView(generics.ListCreateAPIView):
    """
    API view to list all books or create a new book.
    - GET: List all books (publicly available)
    - POST: Create a new book (only for authenticated admin users)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Check if the user is an admin (staff) before creating a book
        if not self.request.user.is_staff:
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        serializer.save()

class BookRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a specific book.
    Only authenticated users can modify books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        # Check if the user is an admin (staff) before updating a book
        if not self.request.user.is_staff:
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        serializer.save()

# 🔹 Student View (UI)
def student_book_list(request):
    """
    Render a page that lists all available books for students.
    """
    books = Book.objects.all()
    return render(request, "books.html", {"books": books})

# 🔹 Admin Signup with Validation
def admin_signup(request):
    """
    Handle admin signup by validating email and password.
    If validation passes, a new admin user is created with a hashed password.
    The user is then logged in automatically.
    """
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        # Validate email format
        if not is_valid_email(email):
            messages.error(request, "Invalid email format.")
            return render(request, "admin_signup.html")

        # Validate password strength
        if not is_valid_password(password):
            messages.error(request, "Password must be at least 6 characters long.")
            return render(request, "admin_signup.html")

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, "admin_signup.html")

        # Create user with hashed password and mark as staff (admin)
        user = User.objects.create(email=email, password=make_password(password), is_staff=True)
        login(request, user)  # Automatically log the user in
        messages.success(request, "Signup successful! You are now logged in.")
        return redirect("admin_books")

    return render(request, "admin_signup.html")

# 🔹 Admin Login
def admin_login(request):
    """
    Handle admin login. Authenticate the user based on email and password.
    If authentication is successful, log the user in and redirect to admin books page.
    Otherwise, show an error message.
    """
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)

        if user:
            login(request, user)
            return redirect("admin_books")
        else:
            messages.error(request, "Invalid email or password.")

    return render(request, "admin_login.html")

# 🔹 Admin Book Management Views (UI)
@login_required
def admin_books(request):
    """
    Display a list of all books for admin management.
    Only accessible to logged-in admin users.
    """
    books = Book.objects.all()
    return render(request, "admin_books.html", {"books": books})

@login_required
def add_book(request):
    """
    Allow admin to add a new book by submitting a form.
    After adding, redirect to the admin books page.
    """
    if request.method == "POST":
        Book.objects.create(
            title=request.POST["title"],
            author=request.POST["author"],
            published_date=request.POST["published_date"],
            isbn=request.POST["isbn"],
            quantity=request.POST["quantity"]
        )
        return redirect("admin_books")
    return render(request, "add_book.html")

@login_required
def update_book(request, book_id):
    """
    Allow admin to update an existing book's details.
    Load the current book data into the form.
    After updating, save the changes and redirect to the admin books page.
    """
    book = get_object_or_404(Book, id=book_id)

    if request.method == "POST":
        book.title = request.POST["title"]
        book.author = request.POST["author"]
        book.published_date = request.POST["published_date"]
        book.isbn = request.POST["isbn"]
        book.quantity = request.POST["quantity"]
        book.save()
        return redirect("admin_books")

    return render(request, "update_book.html", {"book": book})

@login_required
def delete_book(request, book_id):
    """
    Allow admin to delete a book.
    After deletion, redirect to the admin books page.
    """
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return redirect("admin_books")

# 🔹 Logout View
@login_required
def logout_view(request):
    """
    Log out the current user and display a logout success message.
    Redirect the user to the admin login page.
    """
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect("admin_login")
