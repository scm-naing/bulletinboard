from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.active = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = None
    name = models.CharField(max_length=30)
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True
    )
    password = models.CharField(max_length=255)
    profile = models.CharField(max_length=255)
    USER_TYPE = (("0", "Admin"), ("1", "User"))
    type = models.CharField(
        max_length=1,
        choices=USER_TYPE,
        blank=False,
        default="1",
    )
    phone = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=255, null=True)
    dob = models.DateField(null=True, blank=True)
    created_user_id = models.IntegerField(default=1)
    updated_user_id = models.IntegerField(default=1)
    delete_user_id = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(null=True, blank=True)

    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # Email & Password are required by default.
    objects = UserManager()

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True


class Post(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    POST_STATUS = (("0", "inactive"), ("1", "active"))
    status = models.CharField(
        max_length=1,
        choices=POST_STATUS,
        blank=False,
        default="1",
    )
    user = models.ForeignKey("User", on_delete=models.SET_NULL, null=True)
    created_user_id = models.IntegerField()
    updated_user_id = models.IntegerField()
    delete_user_id = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return self.title
