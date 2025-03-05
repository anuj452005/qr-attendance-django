# QR Code Attendance System

A Django-based QR code attendance system for educational institutions. This system allows teachers to generate QR codes for attendance and students to mark their attendance by scanning these QR codes.

## Features

- Multi-role authentication (Admin, Teacher, Student)
- QR code generation for attendance
- Real-time attendance tracking
- Location verification
- Comprehensive reporting
- User management
- Timetable management

## Tech Stack

- Django 5.1.6
- Bootstrap 5
- SQLite (Development) / PostgreSQL (Production)
- JavaScript (for QR code scanning)

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   ```
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Run migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```
6. Create a superuser:
   ```
   python manage.py createsuperuser
   ```
7. Run the development server:
   ```
   python manage.py runserver
   ```

## Project Structure

- `accounts`: User authentication and management
- `administration`: System settings and configuration
- `students`: Student management
- `teachers`: Teacher management
- `academics`: Subjects and departments
- `attendance`: Attendance records and QR code generation
- `timetable`: Class schedules and timetables
- `api`: API endpoints for mobile integration
- `core`: Core functionality and utilities

## License

This project is licensed under the MIT License - see the LICENSE file for details.
