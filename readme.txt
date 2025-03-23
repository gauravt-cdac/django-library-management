Library Management System
=========================

A Django-based Library Management System that allows an admin to manage books (CRUD operations)
and provides a student view to list all available books.

Features:
---------
Admin Operations:
  - Signup & Login (Email & Password Authentication)
  - Create, Read, Update, and Delete (CRUD) book records via API

Student View:
  - Retrieve a list of all books

Authentication & Security:
  - Token-based authentication for admin actions
  - Proper error handling with appropriate HTTP status codes

Tech Stack:
-----------
- Backend: Django, Django REST Framework
- Database: MySQL
- Authentication: Token-based authentication
- Frontend (Optional): Django templates / React / Any framework of choice

Installation & Setup:
---------------------
1. Clone the Repository:
   git clone https://github.com/gauravt-cdac/django-library-management.git
   cd library-management

2. Set Up a Virtual Environment (if not already set):
   On Windows:
     env\Scripts\activate

3. Install Dependencies:
   pip install -r requirements.txt

4. Configure the Database:
   Open settings.py and update the MySQL database settings:

   DATABASES = {
       'default': {
           'ENGINE':   'django.db.backends.mysql',     # Database engine
           'NAME':     'library_db',                   # Your database name
           'USER':     '*****',                        # Your MySQL username
           'PASSWORD': '*****',                        # Your MySQL password
           'HOST':     'localhost',                    # Change if using a remote database
           'PORT':     '3306',                         # Default MySQL port
       }
   }

   After updating the database settings, apply migrations:

   python manage.py makemigrations
   python manage.py migrate

5. Create a Superuser:
   
   python manage.py createsuperuser

   (Follow the prompts to set up an admin user.)

6. Start the Server:

   python manage.py runserver

   The application will be available at: http://127.0.0.1:8000

API Endpoints:
--------------
Authentication:
---------------
- POST /signup/   : Register a new admin
- POST /login/    : Admin login (returns token)

Book Management (Admin):
------------------------
- POST /api/books/          : Add a new book
- GET /api/books/           : Retrieve all books
- GET /api/books/{id}/      : Retrieve a specific book
- PUT /api/books/{id}/      : Update a book record
- DELETE /api/books/{id}/   : Delete a book

Student View:
-------------
- GET /api/books/           : Retrieve all books (public)

Running Tests:
--------------
To ensure everything is working correctly, run:

   python manage.py test

This will execute unit and integration tests for authentication, CRUD operations, and permissions.

Authentication & Security Details:
------------------------------------
- Token-Based Authentication is implemented using Django REST Framework's Token Auth.
- Proper Error Handling ensures clear messages for invalid requests (e.g., duplicate admins, invalid credentials).
- Permissions restrict book management actions to admins only.
