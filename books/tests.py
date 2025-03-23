from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Book
import datetime

User = get_user_model()

class LibraryManagementTests(TestCase):
    def setUp(self):
        """
        Set up the test environment:
        - Create an APIClient instance for making API requests.
        - Create a superuser to simulate an admin user.
        - Force the client to authenticate with the admin user.
        - Create a sample book record to be used in tests.
        """
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(email="admin@test.com", password="admin123")
        self.client.force_authenticate(user=self.admin_user)
        
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            published_date=datetime.date(2024, 1, 1),
            isbn="1234567890123",
            quantity=5
        )

    def tearDown(self):
        """
        Clean up after each test by deleting all book and user records.
        """
        Book.objects.all().delete()
        User.objects.all().delete()

    def test_admin_can_create_book(self):
        """
        Test that an authenticated admin can create a new book via the API.
        """
        url = reverse("book-list")  # URL for listing/creating books
        response = self.client.post(url, {
            "title": "New Book",
            "author": "New Author",
            "published_date": "2024-03-22",
            "isbn": "9876543210987",
            "quantity": 10
        })
        
        # Check that the book is created successfully (HTTP 201)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Verify the response data contains correct book details
        self.assertEqual(response.data["title"], "New Book")
        self.assertEqual(response.data["author"], "New Author")

    def test_admin_can_read_books(self):
        """
        Test that an authenticated admin can retrieve the list of books.
        """
        url = reverse("book-list")  # URL for listing books
        response = self.client.get(url)
        # Check that the response is OK (HTTP 200)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_can_update_book(self):
        """
        Test that an authenticated admin can update an existing book.
        """
        url = reverse("book-detail", args=[self.book.id])  # URL for specific book detail
        response = self.client.put(url, {
            "title": "Updated Book",
            "author": "Updated Author",
            "published_date": "2024-03-22",
            "isbn": "1234567890123",  # Keep same ISBN to update the same book
            "quantity": 8
        })
        
        # Check that the update was successful (HTTP 200)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verify that the book title was updated correctly
        self.assertEqual(response.data["title"], "Updated Book")

    def test_admin_can_delete_book(self):
        """
        Test that an authenticated admin can delete a book.
        """
        url = reverse("book-detail", args=[self.book.id])  # URL for specific book detail
        response = self.client.delete(url)
        # Check that the deletion was successful (HTTP 204 No Content)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_student_can_view_books(self):
        """
        Test that a student (unauthenticated user) can view the list of books.
        """
        # Remove authentication to simulate a student view
        self.client.force_authenticate(user=None)
        url = reverse("book-list")  # URL for listing books
        response = self.client.get(url)
        # Check that the student can access the books (HTTP 200 OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
