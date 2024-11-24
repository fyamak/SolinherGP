from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    # username, first_name, last_name, email, is_staff, is_active, date_joined, last_login, is_superuser, groups, user_permissions
    username = None
    
    ROLE_CHOICES = (
        ('employee', 'Employee'),
        ('engineer', 'Engineer'),
        ('manager', 'Manager'),
        ('operator', 'Operator'),
        ('technician', 'Technician'),
        ('hr', 'Human Resource'),
    )

    email = models.EmailField(_("email address"), unique=True)
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='user')
    # profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    profile_picture = models.CharField(max_length=155,null=True, blank=True) # Pillow lib is necessary
    is_account_verified = models.BooleanField(default=False)
    questions_asked = models.IntegerField(default=0)  
    answers_given = models.IntegerField(default=0)
    receive_email_notifications = models.BooleanField(default=False)
    

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email