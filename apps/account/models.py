from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator


# Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, name, phone, password=None, **extra_fields):
        """
        Creates and saves a User with the given email, name, phone and password.
        """
        if not email:
            raise ValueError('User must have an email address')

        if not name:
            raise ValueError('User must have a name')

        if not phone:
            raise ValueError('User must have a phone number')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            phone=phone,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, phone, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email, name, phone and password.
        """
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_admin=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, name, phone, password, **extra_fields)


# Custom User Model
class User(AbstractBaseUser, PermissionsMixin):
    # UAE phone number validator
    phone_regex = RegexValidator(
        regex=r'^\+971[5]\d{8}$',
        message="Phone number must be in the format: '+9715XXXXXXXX'."
    )

    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=200)
    phone = models.CharField(
        max_length=15,
        validators=[phone_regex],
        unique=True,
        help_text="UAE phone number in format: +9715XXXXXXXX"
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'