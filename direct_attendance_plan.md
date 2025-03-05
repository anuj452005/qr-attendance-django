# Direct QR Code Attendance System Implementation Plan

## Overview
This plan outlines the implementation of a direct QR code attendance system that allows students to mark attendance by scanning QR codes with their native camera apps, without requiring camera permissions in the web application.

## Implementation Tasks

### 1. Database Changes

- [ ] Create a new model `AttendanceToken` with the following fields:
  - `token` (CharField): Unique token for the attendance session
  - `timetable` (ForeignKey): Link to the timetable entry
  - `created_at` (DateTimeField): When the token was created
  - `expires_at` (DateTimeField): When the token expires
  - `is_used` (BooleanField): Whether the token has been used
  - `created_by` (ForeignKey): Teacher who created the token

### 2. Backend Implementation

#### URL Configuration
- [ ] Add new URL patterns in `attendance/urls.py`:
  - `direct-mark/<str:token>/` - For handling direct attendance marking

#### View Functions
- [ ] Create a new view function `generate_attendance_qr` that:
  - Generates a unique token
  - Creates an `AttendanceToken` record
  - Generates a QR code with the full URL
  - Returns the QR code image to the teacher

- [ ] Create a new view function `direct_mark_attendance` that:
  - Validates the token
  - Checks if the user is authenticated
  - Redirects to login if not authenticated
  - Marks attendance if authenticated
  - Shows confirmation page

#### Authentication Handling
- [ ] Modify the login view to accept a `next` parameter
- [ ] Ensure redirect back to the attendance marking page after login

### 3. Frontend Implementation

#### QR Code Display
- [ ] Update the QR code display template to show instructions for students
- [ ] Add information about using native camera apps

#### Attendance Confirmation Page
- [ ] Create a new template for attendance confirmation
- [ ] Show success/error messages
- [ ] Add link to return to student dashboard

### 4. Security Enhancements

- [ ] Implement token expiration (5-10 minutes)
- [ ] Make tokens one-time use only
- [ ] Add rate limiting to prevent abuse
- [ ] Implement proper validation and error handling

### 5. Testing

- [ ] Test with different mobile devices and cameras
- [ ] Test the authentication flow
- [ ] Test token expiration and one-time use
- [ ] Test with different user roles (student, teacher, admin)

### 6. Documentation

- [ ] Update user documentation for teachers
- [ ] Update user documentation for students
- [ ] Document the API endpoints and token system

## Technical Details

### Token Generation
```python
import uuid
import datetime
from django.utils import timezone

def generate_token():
    token = uuid.uuid4().hex
    expires_at = timezone.now() + datetime.timedelta(minutes=10)
    return token, expires_at
```

### URL Structure
The QR code will contain a URL in the format:
```
http://your-domain.com/attendance/direct-mark/[token]/
```

### User Flow
1. Teacher generates QR code for a class
2. Student scans QR code with native camera app
3. Browser opens with the attendance URL
4. If not logged in, student is redirected to login
5. After login, student is redirected back to attendance URL
6. System verifies the token and marks attendance
7. Student sees confirmation message

## Implementation Timeline

### Phase 1: Core Functionality
- Database model creation
- Basic view functions
- QR code generation with URLs

### Phase 2: Authentication Flow
- Login redirect functionality
- Session handling
- Token validation

### Phase 3: UI Enhancements
- Mobile-friendly templates
- Improved user feedback
- Error handling

### Phase 4: Security and Testing
- Token security enhancements
- Comprehensive testing
- Documentation updates
