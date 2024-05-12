Web Engineering - User Management System

This project forms the foundational phase of system development, integrating essential functionalities that allow users to interact effectively with the platform. 
It supports user registration, login, and extensive user management features. Authenticated users can perform CRUD (Create, Read, Update, Delete) operations on user data, 
delivering a robust and efficient user management experience.

Introduction
This web application represents a comprehensive solution designed to manage and secure user data effectively. Utilizing Flask as the server framework and PostgreSQL for database management,
this project focuses on creating a secure environment where user interactions are both safe and efficient. The system employs hashed passwords and cookies to ensure that routes and user sessions are securely managed, providing a reliable and user-friendly interface for administrative tasks.

Technologies Being Used

Backend

Flask: Serves as the backbone of the web application, handling requests and responses, routing, and server-side logic.
PostgreSQL: Used for database management, it stores and retrieves all user data as requested by the application logic, ensuring robust data handling.

Frontend

The project utilizes HTML, CSS, and JavaScript to deliver a responsive and intuitive user interface, providing users with a seamless interaction experience.
Security
Hashed Passwords: To enhance security, the application implements hashed passwords, ensuring that user credentials are stored securely in the database.
Cookies: Used for managing sessions and maintaining user state across different pages of the application.

Packages
Flask-Login: Manages user authentication, providing tools for logging in and out users from the application.
Flask-Migrate: Used for handling SQLAlchemy database migrations for Flask applications.
Psycopg2: A PostgreSQL database adapter for Python, which allows interaction between the Python code and the database.
Flask-Bcrypt: Provides hashing utilities for Flask applications to help safely store user passwords.

Login:
This version substantially enhances the security framework of the system by integrating a sophisticated login mechanism. Instead of using JWT, this system employs hashed passwords for verifying 
user credentials, ensuring that stored passwords are not in plain text, thereby fortifying the security against unauthorized access.
![image](https://github.com/adanielloza/AdminFlaskProject/assets/123408012/7a77821a-d5c6-487b-9391-609e28c2150e)

Admin:

Admin Dashboard:
Admin has the capability to perform CRUD operations on Users, Jobs, Tasks, and Bonifications.
Each section (Users, Jobs, Tasks, Bonifications) will have its own interface for creating, reading, updating, and deleting entries.
Supervisor Dashboard:
Supervisor can view information related to Jobs, Tasks, and Bonifications but does not have CRUD capabilities.

Here's how this structure can be visualized in a flowchart:

The Start point leads to a login verification.
Post-login, the system checks the role of the user.
Depending on the role (Admin or Supervisor), the user is redirected to the respective dashboard.
The Admin Dashboard allows full CRUD operations.
The Supervisor Dashboard allows viewing capabilities only.

![image](https://github.com/adanielloza/AdminFlaskProject/assets/123408012/91393d4a-f043-4d05-b818-b43fe73ab247)



