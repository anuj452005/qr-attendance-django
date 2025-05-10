from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import CustomUser

class Command(BaseCommand):
    help = 'Creates demo users for admin, teacher, and student roles'

    def handle(self, *args, **kwargs):
        User = get_user_model()

        # Create admin user
        if not User.objects.filter(username='admin1').exists():
            admin_user = User.objects.create_user(
                username='admin1',
                email='admin@example.com',
                password='admin123',
                first_name='Admin',
                last_name='User',
                user_type='ADMIN',
                is_staff=True,
                is_superuser=True
            )
            self.stdout.write(self.style.SUCCESS(f'Admin user created: {admin_user.username}'))
        else:
            self.stdout.write(self.style.WARNING('Admin user already exists'))

        # Create teacher user
        if not User.objects.filter(username='teacher1').exists():
            teacher_user = User.objects.create_user(
                username='teacher1',
                email='teacher@example.com',
                password='teacher123',
                first_name='Teacher',
                last_name='User',
                user_type='TEACHER'
            )
            self.stdout.write(self.style.SUCCESS(f'Teacher user created: {teacher_user.username}'))
        else:
            self.stdout.write(self.style.WARNING('Teacher user already exists'))

        # Create student user
        if not User.objects.filter(username='student1').exists():
            student_user = User.objects.create_user(
                username='student1',
                email='student@example.com',
                password='student123',
                first_name='Student',
                last_name='User',
                user_type='STUDENT'
            )
            self.stdout.write(self.style.SUCCESS(f'Student user created: {student_user.username}'))
        else:
            self.stdout.write(self.style.WARNING('Student user already exists'))
