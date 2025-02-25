from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password = None, **extra_fields):
        if not email:
            raise ValueError("Email is required...!")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)          #This ensures the password is stored securely in the database.
        user.save(using=self._db)     #Saves the user instance to the database using the default database connection
        return user                      #Returns the newly created user 
         
# '''BaseUserManager is Django's base class for custom user managers.
# It provides helper methods for handling user authentication and password management.'''
        
    def create_superuser(self, email, password=None, **extra_fields):
            """
            Create and return a superuser with the given email and password. 
            """
            extra_fields.setdefault('is_staff', True)             #Allows access to the Django admin site.
            extra_fields.setdefault('is_superuser', True)         #Grants all permissions.
            extra_fields.setdefault('is_active', True)                 #Ensures the account is active by default.
            return self.create_user(email, password, **extra_fields)