from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# -------------------------------
# 🔹 Custom User Manager
# -------------------------------
class UserManager(BaseUserManager):
    """Custom manager for AdminUser model."""

    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and returns a regular user with an email and password.
        
        Steps:
        1. Check that an email is provided.
        2. Normalize the email (e.g., lowercases the domain).
        3. Create a new user instance with extra fields.
        4. Set the user's password (which hashes it).
        5. Save the user in the database.
        """
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)  # Normalize the email address
        user = self.model(email=email, **extra_fields)  # Create a new user instance
        user.set_password(password)  # Hash and set the password
        user.save(using=self._db)  # Save the user to the database
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and returns a superuser with all privileges.
        
        It sets is_staff and is_superuser to True and checks that they are correctly set.
        """
        extra_fields.setdefault("is_staff", True)      # Ensure the user is marked as staff
        extra_fields.setdefault("is_superuser", True)  # Ensure the user has superuser privileges

        if not extra_fields.get("is_staff"):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

# -------------------------------
# 🔹 Admin User Model
# -------------------------------
class AdminUser(AbstractUser):
    """
    Custom AdminUser model that uses email as the unique identifier instead of a username.
    """
    email = models.EmailField(unique=True)  # Email must be unique for each admin user
    username = None  # Remove the default username field

    USERNAME_FIELD = "email"  # Use email to log in
    REQUIRED_FIELDS = []  # No additional fields are required

    objects = UserManager()  # Use our custom manager for user creation

    def __str__(self):
        """
        Return the email of the user as its string representation.
        """
        return self.email

# -------------------------------
# 🔹 Book Model
# -------------------------------
class Book(models.Model):
    """
    Model to represent books in the library system.
    """
    title = models.CharField(max_length=255)  # The title of the book
    author = models.CharField(max_length=255)  # The author of the book
    published_date = models.DateField(null=True, blank=True)  # Publication date (optional)
    isbn = models.CharField(max_length=13, unique=True, blank=True, null=True)  # Unique ISBN identifier (optional)
    quantity = models.PositiveIntegerField(default=1)  # Number of copies available (default is 1)

    def __str__(self):
        """
        Return a simple string representation: 'Title by Author'.
        """
        return f"{self.title} by {self.author}"
