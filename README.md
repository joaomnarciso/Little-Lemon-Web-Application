# Little Lemon Web Application

## Introduction
This is the final project for the Meta Back-End Developer Capstone course. (https://www.coursera.org/learn/back-end-developer-capstone/)

This web application utilizes Django, Django Rest Framework (DRF), Djoser, and MySQL to manage the backend of a restaurant ordering system. It features simple APIs for managing menu items and booking reservations.

The web app includes:
- A static page available at: [http://localhost:8000](http://localhost:8000)

## Setup Instructions

### 1. Clone the Repository
First, clone the project to your local machine:

git clone git@github.com:joaomnarciso/Little-Lemon-Web-Application.git

### 2. Install Dependencies
Navigate to the project folder and create a virtual environment:

cd Little-Lemon-Web-Application
python3 -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate  # For Windows
Then, install the required dependencies:

pip install -r requirements.txt

### 3. Set Up Database Credentials
In your project, the database connection settings are defined in the settings.py file. You will need to set up your MySQL credentials in this file.

Open restaurant/settings.py and update the DATABASES section with your MySQL credentials:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'your_database_name',
        'USER': 'your_database_user',
        'PASSWORD': 'your_database_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
Make sure your MySQL server is running and accessible.

### 4. Run Migrations
Once your database is configured, you need to apply the migrations to set up the database schema:

python manage.py migrate

### 5. Ensure Djoser Is Installed
Djoser should already be included in the requirements.txt file, but if it's missing, you can install it by running:

pip install djoser

### 6. Create Super Admin and Token for Authentication
To create a superuser (admin) and obtain a token for authentication, follow these steps:

Create a superuser by running:
python manage.py createsuperuser
You can also create other users by using Djoser APIs or through the Django admin panel (http://localhost:8000/admin).
Once the superuser is created, generate an authentication token by sending a POST request to the auth/token/login/ endpoint:
Example payload for Insomnia or Postman:

URL: http://127.0.0.1:8000/auth/token/login/

Payload:

{
  "username": "admin",
  "password": "your_superuser_password"
}
The response will include a token that you need to include in the Authorization header for subsequent requests.

### 7. Running the Development Server
To run the application locally, use the Django development server:

python manage.py runserver
Visit http://127.0.0.1:8000/ to interact with the application.

## API Endpoints

### 1. Menu Items
GET /restaurant/api/menu/: Allows authenticated users to view the list of menu items.
POST /restaurant/api/menu/: Only admin users can create new menu items. Fields required:
title: string
price: decimal
featured: (optional) boolean, default = false
Example POST data:

{
  "title": "Spaghetti",
  "price": 12.99,
  "featured": true
}
GET /restaurant/api/menu/<int:pk>/: Allows authenticated users to view a specific menu item by id.
PUT /restaurant/api/menu/<int:pk>/: Only admin users can update a menu item.
DELETE /restaurant/api/menu/<int:pk>/: Only admin users can delete a menu item.

### 2. Bookings
GET /restaurant/api/book/: Allows authenticated users to list their bookings. Non-admin users will only see their own bookings.
POST /restaurant/api/book/: Allows authenticated users to create a new booking. The name field should match the username. Fields required:
name: string (must match username)
guest_number: (optional) integer, default = 1
date: date in "YYYY-MM-DD" format
comment: (optional) text
Example POST data:

{
  "name": "customer1",
  "guest_number": 2,
  "date": "2024-12-25",
  "comment": "Table by the window"
}
GET /restaurant/api/book/<int:pk>/: Only admin users can view a specific booking by id.
DELETE /restaurant/api/book/<int:pk>/: Only admin users can delete a booking.
Testing the API

You can use the Insomnia client to test the API endpoints. Here's what you need to do:

Make sure you have created a superuser or a regular user and obtained the authentication token.
Add the token to the Authorization header as follows:
Header Key: Authorization
Header Value: Token <your_token_here>
Example:

Authorization: Token 123456abcdef
Test Data for API
Superuser:
Username: admin
Password: 123
Customer:
Username: customer1
Password: lemon@123!
Username: customer2
Password: lemon@123!
Running Tests

To run the tests for your project, use:

python manage.py test
This will run all the tests defined in your project, including tests for the APIs, models, and views.
