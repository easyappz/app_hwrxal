from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    """
    Custom user manager where email is the unique identifier
    for authentication instead of username.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a regular user with the given email and password.
        """
        if not email:
            raise ValueError("The Email field must be set")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a superuser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model that uses email as the username field.
    Designed to be easily extensible for additional fields and role-based access control.
    """

    # Basic authentication field
    email = models.EmailField(
        verbose_name="Email address",
        max_length=255,
        unique=True,
        db_index=True,
    )

    # Personal information fields
    first_name = models.CharField(
        verbose_name="First name",
        max_length=150,
        blank=True,
    )
    last_name = models.CharField(
        verbose_name="Last name",
        max_length=150,
        blank=True,
    )

    # Status fields
    is_active = models.BooleanField(
        verbose_name="Active",
        default=True,
        help_text="Designates whether this user should be treated as active. "
        "Unselect this instead of deleting accounts.",
    )
    is_staff = models.BooleanField(
        verbose_name="Staff status",
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )

    # Timestamp fields
    date_joined = models.DateTimeField(
        verbose_name="Date joined",
        default=timezone.now,
    )
    updated_at = models.DateTimeField(
        verbose_name="Updated at",
        auto_now=True,
    )

    # ### EXTENSIBILITY SECTION ###
    # Add additional profile fields below this comment
    # Examples:
    # phone_number = models.CharField(max_length=20, blank=True)
    # avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    # bio = models.TextField(blank=True)
    # birth_date = models.DateField(blank=True, null=True)
    # ### END EXTENSIBILITY SECTION ###

    # ### ROLE-BASED ACCESS CONTROL SECTION ###
    # Add role-related fields below this comment when expanding RBAC
    # Examples:
    # role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='user')
    # permissions_level = models.IntegerField(default=1)
    # department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, blank=True)
    # ### END RBAC SECTION ###

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # Email is already required by default

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-date_joined"]
        db_table = "users"

    def __str__(self):
        return self.email

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name or self.email

    def get_short_name(self):
        """
        Return the short name for the user.
        """
        return self.first_name or self.email
