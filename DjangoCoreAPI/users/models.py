from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager
import os
from django.conf import settings


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
    profile_picture = models.ImageField(blank=True, null=True, upload_to="temp/") 
    is_account_verified = models.BooleanField(default=False)
    questions_asked = models.IntegerField(default=0)  
    answers_given = models.IntegerField(default=0)
    receive_email_notifications = models.BooleanField(default=False)
    

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    
    def save(self, *args, **kwargs):
        # Check if the user already exists (has an ID)
        is_new = not self.pk
        previous_photo = None

        if not is_new:
            # Retrieve the previous photo file name before saving
            previous_photo = CustomUser.objects.filter(pk=self.pk).values('profile_picture').first().get('profile_picture')

        super().save(*args, **kwargs)  # Save the user to get an ID
        
        # Rename and move the profile picture if it's uploaded
        if self.profile_picture:
            old_path = self.profile_picture.path
            ext = os.path.splitext(old_path)[1]  # Get the file extension (e.g., .jpg)
            new_filename = f"user_{self.id}{ext}"  # Rename to user_<id>.<ext>
            new_path = os.path.join(settings.MEDIA_ROOT, "profile", new_filename)
            
            # Create the 'profile' directory if it doesn't exist
            os.makedirs(os.path.dirname(new_path), exist_ok=True)
            
            # Move and rename the file
            os.rename(old_path, new_path)
            
            # Update the profile_picture field with the new path
            self.profile_picture.name = f"profile/{new_filename}"
            super().save(update_fields=['profile_picture'])  # Save the updated path
            
            # Delete the previous profile picture file if it exists and is different
            if previous_photo and previous_photo != self.profile_picture.name:
                old_photo_path = os.path.join(settings.MEDIA_ROOT, previous_photo)
                if os.path.exists(old_photo_path):
                    os.remove(old_photo_path)
    
    objects = CustomUserManager()

    def __str__(self):
        return self.email