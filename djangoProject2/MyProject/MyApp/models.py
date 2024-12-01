from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('team_member', 'Team Member'),
        ('project_leader', 'Project Leader'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='team_member')
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

def __str__(self):
        return self.username
