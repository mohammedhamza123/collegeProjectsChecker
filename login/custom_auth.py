from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from api.models import Student

User = get_user_model()


class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Check if username is a valid username
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            try:
                # Check if username is a valid SerialNumber in the Student model
                if not username.isdigit():
                    return None
                student = Student.objects.get(serialNumber=username)
                user = student.user
            except Student.DoesNotExist:
                return None

        if user.check_password(password):
            # Check if user is a student and if approval is required
            try:
                student = Student.objects.get(user=user)
                # If student is not approved, return None (authentication fails)
                if not student.is_approved:
                    return None
            except Student.DoesNotExist:
                # User is not a student, allow authentication
                pass
            
            return user

        return None
